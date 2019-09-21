import cv2
import numpy as np
import os
from utils import imageFuncs
from Component import Component
os.system('clear')

boardX = 39 # squares
boardY = 63 # squares

components = []
components.append(Component('arduino', 0, 100, 0))
components.append(Component('diode', 200, 100, 0))
components.append(Component('led', 150, 50, 0))
components.append(Component('SOIC8', 30, 50, 0))


# load the board image and scale it down
board = cv2.imread('images/board.png', cv2.IMREAD_COLOR)
height = int(63 * 3.1667)
width = int(height * boardY / boardX)
board = cv2.resize(board,(width, height))

for component in components:
    board = imageFuncs.insertComponent(board, component)


cv2.imshow('Final image', board)
cv2.waitKey(0)
cv2.destroyAllWindows()