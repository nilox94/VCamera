import cv2


def opencv_preview(vcam):
    while True:
        src = vcam.queue.get()
        tr = vcam.queue.get()
        cv2.imshow("original camera", src)
        cv2.imshow("virtual camera", tr)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            vcam.stop()
            vcam.terminate()
            break
