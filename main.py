import cv2
import numpy as np
import os
from utils import imageFuncs
from Component import Component
import pandas as pd
import csv


os.system('clear')

pinlist = ['arduino1', 'arduino2', 'arduino3', 'arduino4', 'arduino5', 'arduino6', 'arduino7', 'arduino8', 'arduino9', 'arduino10', 'arduino11', 'arduino12', 'arduino13', 'arduino14', 'arduino15', 'arduino16', 'resistor1', 'resistor2']

df = pd.DataFrame(0, index=pinlist, columns=pinlist)
df['arduino15']['resistor1'] = 1
df['resistor1']['arduino15'] = 1

# 1. LOAD BOARD IMAGE AND BOARD MATRIX
boardImage = cv2.imread('images/board.png', cv2.IMREAD_UNCHANGED)
print("Board image width: " + str(boardImage.shape[1]) + ", board image height: " + str(boardImage.shape[0]))
boardMatrix = np.zeros((39*2, 63*2), dtype=np.int)
print("Board matrix width: " + str(boardMatrix.shape[1]) + ", board matrix height: " + str(boardMatrix.shape[0]) + '\n')



# 2. PLACE ARDUINO ON IMAGE AND ARRAY IN PREDEFINED LOCATION
# MAKE SURE ARDUINO MATRIX HAS EMPTY ROW ON TOP
arduinoImage = cv2.imread('images/arduino.png', cv2.IMREAD_UNCHANGED)
arduinoMatrix = pd.read_csv('components/arduino.csv')

boardImage = imageFuncs.insertImage(boardImage, arduinoImage, 0, 23, 0)
boardMatrix = imageFuncs.insertMatrix(boardMatrix, arduinoMatrix, 0, 23, 0)




# 3. ITERATE THROUGH ARDUINO PINS, PLACE ALL 2 PIN COMPONENTS ON THE ARDUINO PINS
for pin in pinlist:

	# ignore non arduino pins
	if (not 'arduino' in pin):
		continue

	# ignore unconnected pins
	if (sum(df[pin]) == 0):
		continue

	print(df[pin])
	













# for row in boardMatrix:
# 	print(', '.join(str(row)))













# components = []
# components.append(Component('arduino', 100, 100, 45))
# components.append(Component('diode', 50, 30, 0))
# components.append(Component('led', 250, 100, 0))
# components.append(Component('SOIC8', 20, 30, 0))


# # load the board image and scale it down


# # iterate through the components and put them on the board
# for component in components:
#     board = imageFuncs.insertComponent(board, component)


# imageFuncs.printMatrix(boardMatrix)
cv2.imshow('Board image', boardImage)
cv2.waitKey(0)
cv2.destroyAllWindows()