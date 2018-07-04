import cv2
import numpy as np


def bgr2yuyv(bgr_frame):
    yuv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV).reshape(-1)
    buff = np.empty(bgr_frame.size*2//3, dtype=np.uint8)
    buff[0::2] = yuv[0::3]
    buff[1::4] = yuv[1::6]
    buff[3::4] = yuv[2::6]
    return buff

def rgb2yuyv(bgr_frame):
    yuv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV).reshape(-1)
    buff = np.empty(bgr_frame.size*2//3, dtype=np.uint8)
    buff[0::2] = yuv[0::3]
    buff[1::4] = yuv[2::6]
    buff[3::4] = yuv[1::6]
    return buff
