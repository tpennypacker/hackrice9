import helpers
import numpy as np

import cv2
size = (1280, 720)

# Slideshow of background images
slides = {0:cv2.resize(cv2.imread("0.png"), size), 
1:cv2.resize(cv2.imread("1.png"), size), 
2:cv2.resize(cv2.imread("2.png"), size), 
3:cv2.resize(cv2.imread("3.png"), size), 
4:cv2.resize(cv2.imread("4.png"), size)}

slides2 = {1:cv2.resize(cv2.imread("1s.png"), size),
2:cv2.resize(cv2.imread("2s.png"), size),
3:cv2.resize(cv2.imread("3s.png"), size),
4:cv2.resize(cv2.imread("4s.png"), size)}

c = 1
c2 = 0
image_count = 0
cv2.namedWindow("Projector", cv2.WINDOW_NORMAL)
cv2.imshow("Projector", slides[c])

img = None
h = None
h2 = None
bg = False
pts = []
board_pts = []

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Overlays board image on top of slideshow image
def project(imc):
    if bg:
        overlay = cv2.warpPerspective(cv2.imread("output/image" + str(imc) + ".png"), np.linalg.inv(h2), size)
        cv2.imshow("Projector", overlay + slides[0])
    else:
        overlay = cv2.warpPerspective(cv2.imread("output_no_bg/image" + str(imc) + ".png"), np.linalg.inv(h2), size)
        cv2.imshow("Projector", overlay + slides[0])

# Image click handler
def click(event, x, y, flags, param):
    global pts, c, c2, img, h, h2
    if event == cv2.EVENT_LBUTTONDOWN and len(pts) < 4:
        pts.append([x,y])
        print (pts)
        if c <= 3:
            cv2.imshow("Projector", slides[c + 1])
        else:
            h = helpers.calculate_h(pts)
            cv2.imshow("Projector", slides2[c2 + 1])
            c2 += 1
        c += 1
    elif event == cv2.EVENT_LBUTTONDOWN and len(pts) == 4 and len(board_pts) < 4:
        board_pts.append([x,y])
        temp = np.dot(h, np.array([x, y, 1]))
        temp = temp / temp[2]

        print (board_pts)
        if c2 <= 3:
            cv2.imshow("Projector", cv2.circle(slides2[c2 + 1].copy(), (int(temp[0]), int(temp[1])), 5, (0,0,255), 3))
        else:
            cv2.imshow("Projector", cv2.circle(slides2[1].copy(), (int(temp[0]), int(temp[1])), 5, (0,0,255), 3))
        if len(board_pts) == 4:
            proj_board_pts = helpers.get_proj_board_pts(board_pts)
            h2 = helpers.calculate_h2(proj_board_pts)
            project(image_count)
        c2 += 1


cv2.setMouseCallback("image", click)

cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_EXPOSURE, 4) 
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.9)

# Iterate per frame in video.
while True:
    ret, img = cap.read()
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('d'):
        image_count += 1
        if image_count >= 29:
            image_count = 0
        project(image_count)

    if key & 0xFF == ord('a'):
        image_count -= 1
        if image_count < 0:
            image_count = 28
        project(image_count)

    if key & 0xFF == ord('b'):
        bg = not bg
        project(image_count)

    if key & 0xFF == ord('r'):
        board_pts = []
        c2 = 1
        cv2.imshow("Projector", slides2[c2])

    if key & 0xFF == ord('f'):
        board_pts = []
        pts = []
        c = 1
        c2 = 0
        cv2.imshow("Projector", slides[c])

    if key & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break