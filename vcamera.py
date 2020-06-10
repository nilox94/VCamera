#!/usr/bin/env python3
from cv2 import cv2
import os
import fcntl
import v4l2
from multiprocessing import Process
from filters import bgr2yuyv
from preview import opencv_preview
from multiprocessing import Queue, Value
from ctypes import c_bool

DEFAULT_INPUT = "/dev/video0"
DEFAULT_OUTPUT = "/dev/video1"


class VCamera(Process):
    def __init__(
        self,
        in_dev_name=DEFAULT_INPUT,
        out_dev_name=DEFAULT_OUTPUT,
        transform=None,
        queue=False,
    ):
        Process.__init__(self)
        self.in_dev_name = in_dev_name
        self.out_dev_name = out_dev_name
        self.transform = transform or (lambda x: x)
        self.running = Value(c_bool)
        self.queue = Queue(4) if queue else None

    def setup(self):
        # prepare input camera to capture frames
        self.in_dev = cv2.VideoCapture(self.in_dev_name)
        ok, im = self.in_dev.read()
        if not ok:
            raise IOError("Unable to read frames from device %s" % self.in_dev_name)

        # get frame domensions
        height, width, _ = im.shape
        channels = 2

        # open output camera
        if not os.path.exists(self.out_dev_name):
            raise IOError("Device %s does not exist" % self.out_dev_name)
        self.out_dev = open(self.out_dev_name, "wb")

        # get output camera capabilities
        capability = v4l2.v4l2_capability()
        print(
            "Get capabilities result: %s"
            % (fcntl.ioctl(self.out_dev, v4l2.VIDIOC_QUERYCAP, capability))
        )
        print("Capabilities: %s" % hex(capability.capabilities))
        print("V4l2 driver: %s" % capability.driver.decode())

        # set up formatting of output camera
        fmt = v4l2.v4l2_format()
        fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        fmt.fmt.pix.field = v4l2.V4L2_FIELD_NONE
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YUYV
        fmt.fmt.pix.width = width
        fmt.fmt.pix.height = height
        fmt.fmt.pix.bytesperline = width * channels
        fmt.fmt.pix.sizeimage = width * height * channels
        fmt.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_SRGB
        print(
            "Set format result: %d" % fcntl.ioctl(self.out_dev, v4l2.VIDIOC_S_FMT, fmt)
        )

    def run(self):
        self.running.value = True
        self.setup()
        print("Begin loopback write on %s" % self.out_dev_name)
        # RTWL ;)
        while self.running.value:
            # READ
            ok, src = self.in_dev.read()
            if not ok:
                continue
            # TRANSFORM
            tr = self.transform(src)
            tgt = bgr2yuyv(tr)
            # WRITE
            self.out_dev.write(tgt)
            if self.queue is not None and self.queue.qsize() <= self.queue._maxsize - 2:
                self.queue.put(src)
                self.queue.put(tr)
        # LOOP

        print("End loopback write on %s" % self.out_dev_name)
        self.release()

    def release(self):
        self.in_dev.release()
        self.out_dev.close()
        print("Cameras are closed")

    def stop(self):
        self.running.value = False

    def __del__(self):
        del self


if __name__ == "__main__":
    from os import geteuid
    from sys import stderr
    from argparse import ArgumentParser
    from filters import registry

    parser = ArgumentParser("vcamera")
    parser.add_argument(
        "-i",
        default=DEFAULT_INPUT,
        metavar="INPUT_DEVICE",
        dest="input_device",
        help=f"input video device (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "-o",
        default=DEFAULT_OUTPUT,
        metavar="OUTPUT_DEVICE",
        dest="output_device",
        help=f"output video loopback device (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "-f",
        nargs="*",
        choices=registry.filter_names(),
        metavar="FILTER",
        dest="filters",
        help="list of filters to apply (as a pipeline)",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        dest="display_preview",
        help="display virtual camera preview in an opencv window",
    )
    parser.add_argument(
        "-l",
        action="store_true",
        dest="list_filters",
        help="list all available filters",
    )
    args = parser.parse_args()

    if args.list_filters:
        print("filters:", " ".join(registry.filter_names()), sep="\n\t")
        exit()

    if geteuid():
        print("VCamera needs to be root", file=stderr)
        exit(1)

    vcam = VCamera(
        args.input_device,
        args.output_device,
        registry.get(*args.filters),
        args.display_preview,
    )
    vcam.start()
    if args.display_preview:
        opencv_preview(vcam)
    vcam.join()
