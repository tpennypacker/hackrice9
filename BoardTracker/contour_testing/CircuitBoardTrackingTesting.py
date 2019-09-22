import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

def show(title, img, write = False, wait = False):
    """
    Displays image using OpenCV functions.
    """
    cv2.namedWindow(title, flags = cv2.WINDOW_NORMAL)
    cv2.imshow(title, img)
    cv2.resizeWindow(title, 1200, 900)
    if write:
        cv2.imwrite(title + ".png", img)
    if wait:
        cv2.waitKey(1)

def findRect(im):
    boundingBoxes = []
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    #thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]

    #opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    #opening = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    #thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 1)
    
    #show("gray", thresh, False, True)
    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        if cv2.contourArea(cnt) < 5000 or cv2.contourArea(cnt) > 30000:
            continue
        M = cv2.moments(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        vals = np.array(cv2.mean(im[y:y+h,x:x+w])).astype(np.uint8)
        cv2.rectangle(im, (x,y), (x + w, y + h), (0, 255, 0), 3) 
        cv2.putText(im, str(np.array(cv2.mean(im[y:y+h,x:x+w])).astype(np.uint8)), (x + 1, y + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), lineType=cv2.LINE_AA)
        boundingBoxes.append((x, y, x+w, y+h))
        #cv2.imshow("frame", im)
    return boundingBoxes

def findRectt(im):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,5,25,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    print (dst>0.01*dst.max())
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('dst',img)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

img = cv2.imread("test.jpg")
img = cv2.imread("train/IMG_5122.JPG")
im = imutils.resize(img, width=400)
findRectt(im)

def findRecttt():
    MIN_MATCH_COUNT = 10

    img1 = cv2.imread('download.jpg',0)          # queryImage
    img2 = cv2.imread('train/IMG_5122.png',0) # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    matchesMask = None
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()

#findRectt()
