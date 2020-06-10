#!/usr/bin/env python3
import cv2
import os, fcntl
import v4l2
from multiprocessing import Process
from filters import bgr2yuyv
from multiprocessing import Queue, Value
from ctypes import c_bool

virtual = lambda f: f


class VCamera(Process):
    def __init__(
        self,
        in_dev_name="/dev/video0",
        out_dev_name="/dev/video1",
        flip=False,
        queue=False,
    ):
        Process.__init__(self)
        self.in_dev_name = in_dev_name
        self.out_dev_name = out_dev_name
        self.flip = flip
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
        format = v4l2.v4l2_format()
        format.type = v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        format.fmt.pix.field = v4l2.V4L2_FIELD_NONE
        format.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YUYV
        format.fmt.pix.width = width
        format.fmt.pix.height = height
        format.fmt.pix.bytesperline = width * channels
        format.fmt.pix.sizeimage = width * height * channels
        format.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_SRGB
        print(
            "Set format result: %d"
            % fcntl.ioctl(self.out_dev, v4l2.VIDIOC_S_FMT, format)
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
            if self.flip:
                tr = cv2.flip(tr, 1)
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
        print("cameras are closed")

    def stop(self):
        self.running.value = False

    def __del__(self):
        del self

    @virtual
    def transform(self, bgr_frame):
        # override this method in a subclass
        # you can use any of the filters at `filters`
        return bgr_frame


if __name__ == "__main__":
    vcam = VCamera(flip=True)
    vcam.start()
    vcam.join()
