import cv2
import numpy as np

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

    y = int(y * (l_img.shape[0] / 78))
    x = int(x * (l_img.shape[1] / 126))

    # halfY1 = int(s_img.shape[0] / 2)
    # halfX1 = int(s_img.shape[1] / 2)
    # halfY2 = s_img.shape[0] - halfY1
    # halfX2 = s_img.shape[1] - halfX1

    for row in range (0, s_img.shape[0]-1):
        for col in range (0, s_img.shape[1]-1):
            if (len(s_img[row][col]) > 2):
                if (s_img[row][col][3] != 0):
                    l_img[y + row][x + col] = s_img[row][col]
                    #l_img[y-halfY1 + row][x-halfX1 + col] = s_img[row][col]
                    #l_img[y-halfY1:y+halfY2, x-halfX1:x+halfX2] = s_img

    return l_img

def insertMatrix(l_mat, s_mat, x, y, theta):
    l_mat[y:y+s_mat.shape[0], x:x+s_mat.shape[1]] = s_mat
    return l_mat

def insertCircle(l_img, x, y, color):
    y = int(y * (l_img.shape[0] / 78))
    x = int(x * (l_img.shape[1] / 126))
    return cv2.circle(l_img, (x,y), 7, color, -1)

def insertComponent(board, component):
    
    print("Inserting " + component.name + " at  (" + str(component.x) + ", " + str(component.y) + ")")
    componentImg = cv2.imread('images/' + component.name + '.png', cv2.IMREAD_UNCHANGED)
    print("Width: " + str(componentImg.shape[1]) + ", Height: " + str(componentImg.shape[0]) + '\n')
    return insertImage(board, componentImg, component.x, component.y, component.theta)


def printMatrix(matrix):
    for row in matrix:
        print([x for x in row])


def drawSolder(board, x0, y0, x1, y1):
    return cv2.line(board, (x0, y0), (x1, y1), (50,50,50), 1)







