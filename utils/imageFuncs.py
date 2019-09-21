import cv2
import numpy as np
from Component import Component

def boundedRotation(image, angle):
    # grab the dimensions of the image and then determine the center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix, then grab the sine and cosine
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def insertImage(l_img, s_img, x, y, theta):

    s_img = boundedRotation(s_img, theta)

    halfY1 = int(s_img.shape[0] / 2)
    halfX1 = int(s_img.shape[1] / 2)
    halfY2 = s_img.shape[0] - halfY1
    halfX2 = s_img.shape[1] - halfX1

    l_img[y-halfY1:y+halfY2, x-halfX1:x+halfX2] = s_img

    return l_img


def insertComponent(board, component):
    
    print("Inserting " + component.name + " at  (" + str(component.x) + ", " + str(component.y) + ")")
    componentImg = cv2.imread('images/' + component.name + '.png')
    print(componentImg[0, 0])

    print("Width: " + str(componentImg.shape[1]) + ", Height: " + str(componentImg.shape[0]))
    return insertImage(board, componentImg, component.x, component.y, component.theta)


def drawSolder(board, x0, y0, x1, y1):
    return cv2.line(board, (x0, y0), (x1, y1), (50,50,50), 1)