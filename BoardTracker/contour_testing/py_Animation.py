import cv2
import numpy as np
import time

Frame_out = np.zeros((500, 640, 4),np.uint8)

a = 1

while a<255:
    cv2.rectangle(Frame_out,(a,a),(a*2,a*2),(0,0,255-a),0)
    time.sleep(0.05)
    cv2.imshow('Animation', Frame_out)
    cv2.rectangle(Frame_out,(a,a),(a*2,a*2),(0,0,0),0)
    a +=2
    if(a > 254):
        a = 1
    k = cv2.waitKey(10)
    if k == 27:
        break

cv2.destroyAllWindows()
