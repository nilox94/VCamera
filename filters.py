import cv2
import numpy as np


k = np.ones((4, 4), dtype=np.uint8)


def wierd_grad(bgr_frame):
    grad = cv2.morphologyEx(bgr_frame, cv2.MORPH_GRADIENT, k)
    mapped_grad = np.log2(grad - grad.min() + 1) + 1
    mapped_grad = (grad * (255.0 / grad.max())).astype(np.uint8)
    return mapped_grad


a = np.array([[-0.3, -0.1, -0.1], [0.2, 0.7, 0.1], [0.2, 0.2, 0.6]]).T
b = np.array([144, 0, 0], dtype=np.uint8)


def affine_transform(bgr_frame):
    return np.dot(bgr_frame, a).astype(np.uint8) + b


def canny_filter(bgr_frame):
    im = cv2.GaussianBlur(bgr_frame, (13, 13), 10)
    c = cv2.Canny(im, 15, 15)
    return np.dstack((c, c, c))


def filter1(bgr_frame):
    b, g, r = cv2.split(bgr_frame)
    b2 = np.where(0.5 * b > np.abs(g - r), b, np.maximum(g, r))
    g2 = np.where(0.5 * g > np.abs(b - r), g, np.maximum(b, r))
    r2 = np.where(0.5 * r > np.abs(b - g), r, np.maximum(b, g))
    im = np.dstack((b2, g2, r2))
    im = cv2.GaussianBlur(im, (7, 5), 2)
    return im


# YUYV (YUV-4:2:2) conversions


def bgr2yuyv(bgr_frame):
    yuv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV).reshape(-1)
    buff = np.empty(bgr_frame.size * 2 // 3, dtype=np.uint8)
    buff[0::2] = yuv[0::3]
    buff[1::4] = yuv[1::6]
    buff[3::4] = yuv[2::6]
    return buff


def rgb2yuyv(bgr_frame):
    yuv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2YUV).reshape(-1)
    buff = np.empty(bgr_frame.size * 2 // 3, dtype=np.uint8)
    buff[0::2] = yuv[0::3]
    buff[1::4] = yuv[2::6]
    buff[3::4] = yuv[1::6]
    return buff
