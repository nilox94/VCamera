#!/usr/bin/env python3
import cv2
import numpy as np
from vcamera import VCamera
from filters import affine_transform, wierd_grad


class MyVCamera(VCamera):
    """
    Slow motion
    """
    FRAMES = 10
    LAMBDA = .2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prev_frame = None


    def transform(self, bgr_frame):
        if self.prev_frame is None:
            self.prev_frame = bgr_frame

        frame = MyVCamera.LAMBDA * bgr_frame + (1. - MyVCamera.LAMBDA) * self.prev_frame
        self.prev_frame = frame

        return frame.astype(np.uint8)


if __name__ == '__main__':
    vcam = MyVCamera(flip=True)
    vcam.start()
    vcam.join()
