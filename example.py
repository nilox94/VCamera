#!/usr/bin/env python3
import cv2
from vcamera import VCamera
from filters import affine_transform


class AffineVCamera(VCamera):
    def transform(self, bgr_frame):
        return affine_transform(bgr_frame)


vcam = AffineVCamera(flip=True, queue=True)
vcam.start()
while True:
    src = vcam.queue.get()
    tr = vcam.queue.get()
    cv2.imshow('original camera', src)
    cv2.imshow('virtual camera', tr)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        vcam.stop()
        vcam.terminate()
        break
