import cv2
import numpy as np

h = None
h2 = None

# Calculates homography transition matrix from the camera input to the projector output.
def calculate_h(pts_cam):
	global h
	pts_cam = np.array(pts_cam)
	pts_proj = np.array([[102, 78-12], [100,663-12], [1179,663-12], [1179, 77-12]])
	#pts_proj = np.array([[151, 116], [151, 997], [1770, 997],[1770,116]])
	h = cv2.findHomography(pts_cam, pts_proj)[0]
	return h

# Retrieves projected board points given selected camera board points.
def get_proj_board_pts(pts_board_cam):
	print("get_proj_board_pts")
	print(h)
	pts_board_cam = np.array(pts_board_cam)
	proj_board_pts = []
	for pair in pts_board_cam:
		x = np.dot(h, np.array([pair[0], pair[1], 1]))
		x = x / x[2]
		proj_board_pts.append([x[0],x[1]])
	return np.array(proj_board_pts)

# Calculates homography transition matrix from the projected board points input
# to the actual board dimension output.
def calculate_h2(proj_board_pts):
	global h2
	# top left, bottom left, bottom right, top right
	pts_trev = np.array([[0,0], [0, 585], [945, 585], [945, 0]])
	h2 = cv2.findHomography(proj_board_pts, pts_trev)[0]
	return h2