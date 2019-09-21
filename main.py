import cv2
import numpy as np
import os
from utils import imageFuncs
from Component import Component
os.system('clear')

boardX = 39 # squares
boardY = 63 # squares

components = []
components.append(Component('arduino', 100, 100, 0))
components.append(Component('diode', 50, 30, 0))
components.append(Component('led', 250, 100, 0))
components.append(Component('SOIC8', 20, 30, 0))


# load the board image and scale it down
board = cv2.imread('images/board.png', cv2.IMREAD_COLOR)

print("Board width: " + str(board.shape[1]) + ", board height: " + str(board.shape[0]))

# iterate through the components and put them on the board
for component in components:
    board = imageFuncs.insertComponent(board, component)


cv2.imshow('Final image', board)
cv2.waitKey(0)
cv2.destroyAllWindows()