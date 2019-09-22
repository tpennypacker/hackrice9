import cv2
import numpy as np
import os
from utils import imageFuncs
import pandas as pd
import csv
from components import allComponents

ARDUINO_Y = 23
ARDUINO_HEIGHT = 39*2
ARDUINO_WIDTH = 63*2

firstResistor = True
firstShifter = True

imgNum = 0

def showImage(img):
	global imgNum
	# cv2.imshow('Board image', img)
	# cv2.waitKey(0)
	cv2.imwrite('output/image' + str(imgNum) + '.png', img)
	imgNum += 1



os.system('clear')

pinlist = ['arduino1', 'arduino2', 'arduino3', 'arduino4', 'arduino5', 'arduino6', 'arduino7', 'arduino8', 'arduino9', 'arduino10', 'arduino11', 'arduino12', 'arduino13', 'arduino14', 'arduino15', 'arduino16', 'arduino17', 'arduino18', 'arduino19', 'arduino20', 'arduino21', 'arduino22', 'arduino23', 'arduino24', 'arduino25', 'arduino26', 'arduino27', 'arduino28', 'arduino29', 'arduino30', 'resistor1', 'resistor2', 'button1', 'button2', 'buzzer1', 'buzzer2']
adjMatrix = np.zeros((len(pinlist), len(pinlist)))
adjMatrix[pinlist.index('arduino21')][pinlist.index('resistor2')] = 1
adjMatrix[pinlist.index('arduino22')][pinlist.index('resistor2')] = 1
adjMatrix[pinlist.index('arduino5')][pinlist.index('buzzer2')] = 1
adjMatrix[pinlist.index('arduino27')][pinlist.index('button1')] = 1
adjMatrix[pinlist.index('arduino24')][pinlist.index('button1')] = 1

# 1. LOAD BOARD IMAGE AND BOARD MATRIX
boardImage = cv2.imread('images/board.png', cv2.IMREAD_UNCHANGED)


## black background
mask = np.zeros((boardImage.shape[0], boardImage.shape[1], 4), np.uint8)
boardImage = cv2.bitwise_and(boardImage, mask)


print("Board image width: " + str(boardImage.shape[1]) + ", board image height: " + str(boardImage.shape[0]))
boardMatrix = np.zeros((ARDUINO_HEIGHT, ARDUINO_WIDTH), dtype=np.int)
print("Board matrix width: " + str(boardMatrix.shape[1]) + ", board matrix height: " + str(boardMatrix.shape[0]) + '\n')

showImage(boardImage)


# 2. PLACE ARDUINO ON IMAGE AND ARRAY IN PREDEFINED LOCATION
# MAKE SURE ARDUINO MATRIX HAS EMPTY ROW ON TOP
arduinoImage = cv2.imread('images/arduino.png', cv2.IMREAD_UNCHANGED)
arduinoMatrix = pd.read_csv('components/arduino.csv')

boardImage = imageFuncs.insertImage(boardImage, arduinoImage, 0, ARDUINO_Y, 0)
boardMatrix = imageFuncs.insertMatrix(boardMatrix, arduinoMatrix, 0, ARDUINO_Y, 0)
showImage(boardImage)



# 3. ITERATE THROUGH ADJ MATRIX AND FIND CONNECTIONS
for j in range (len(adjMatrix)):
	for i in range (len(adjMatrix[0])):
		if (adjMatrix[j][i] == 1):

			# 4. WE ONLY CARE ABOUT CONNECTIONS BETWEEN THE ARDUINO AND TWO-PIN COMPONENTS
			otherPin = ''
			arduinoPin = ''
			if ('shifter' in pinlist[j] or 'shifter' in pinlist[i] or 'lcd' in pinlist[j] or 'lcd' in pinlist[i]):
				continue
			if (not 'arduino' in pinlist[j] and 'arduino' in pinlist[i]):
				otherPin = pinlist[j]
				arduinoPin = pinlist[i]
			elif ('arduino' in pinlist[j] and not 'arduino' in pinlist[i]):
				otherPin = pinlist[i]
				arduinoPin = pinlist[j]
			else:
				continue

			otherComponent = ''.join(i for i in otherPin if not i.isdigit())
			componentImage = cv2.imread('images/' + otherComponent + '.png', cv2.IMREAD_UNCHANGED)
			componentMatrix = pd.read_csv('components/' + otherComponent + '.csv')
			arduinoPinNumber = pinlist.index(arduinoPin)


			# 5. PLACE THE COMPONENT
			arduinoPinCoord = allComponents.allComponents['arduino'][arduinoPin]
			componentPinCoord = allComponents.allComponents[otherComponent][otherComponent + '1']
			componentHeight = componentMatrix.shape[0]
			componentWidth = componentMatrix.shape[1]
			componentX = arduinoPinCoord[0]+1 -int(componentWidth/2)
			componentY = arduinoPinCoord[1]+1 + ARDUINO_Y
			if (arduinoPinNumber < 15):
				componentY = componentY - int(componentHeight*1.4)
			else:
				componentY = componentY + 2
			boardImage = imageFuncs.insertImage(boardImage, componentImage, componentX, componentY, 0)
			boardMatrix = imageFuncs.insertMatrix(boardMatrix, componentMatrix, componentX, componentY, 0)
			
			# 6. HIGHTLIGHT THE TWO PINS ON A MASK
			mask = np.zeros((boardImage.shape[0], boardImage.shape[1], 4), np.uint8)
			mask = imageFuncs.insertCircle(mask, componentPinCoord[0] + componentX, componentPinCoord[1] + componentY, (255, 255, 255))
			mask = imageFuncs.insertCircle(mask, arduinoPinCoord[0] + 1, arduinoPinCoord[1] + ARDUINO_Y, (255, 255, 255))
			mask = cv2.bitwise_not(mask)
			circleImg = np.zeros((boardImage.shape[0], boardImage.shape[1], 4), np.uint8)
			circleImg = imageFuncs.insertCircle(circleImg, componentPinCoord[0] + componentX, componentPinCoord[1] + componentY, (255, 0, 255))
			circleImg = imageFuncs.insertCircle(circleImg, arduinoPinCoord[0] + 1, arduinoPinCoord[1] + ARDUINO_Y, (255, 0, 255))
			maskedBoard = cv2.bitwise_and(boardImage, mask)
			boardWithDots = cv2.bitwise_or(maskedBoard, circleImg)
			showImage(boardWithDots)

			# 7. HIGHLIGHT THE GROUND NODE (if buzzer or button)
			if (otherComponent == 'buzzer' or otherComponent == 'button'):
				componentPinCoord = allComponents.allComponents[otherComponent][otherComponent + '2']
				mask = np.zeros((boardImage.shape[0], boardImage.shape[1], 4), np.uint8)
				mask = imageFuncs.insertCircle(mask, componentPinCoord[0] + componentX, componentPinCoord[1] + componentY, (255, 255, 255))
				mask = cv2.bitwise_not(mask)
				circleImg = np.zeros((boardImage.shape[0], boardImage.shape[1], 4), np.uint8)
				circleImg = imageFuncs.insertCircle(circleImg, componentPinCoord[0] + componentX, componentPinCoord[1] + componentY, (0, 255, 255))
				maskedBoard = cv2.bitwise_and(boardImage, mask)
				boardWithDots = cv2.bitwise_or(maskedBoard, circleImg)
				showImage(boardWithDots)

			# 7.5 IF IT'S THE FIRST RESISTOR, PLACE THE LED
			elif (firstResistor and otherComponent == 'resistor'):
				firstResistor = False
				componentImage = cv2.imread('images/' + 'led' + '.png', cv2.IMREAD_UNCHANGED)
				boardImage = imageFuncs.insertImage(boardImage, componentImage, componentX - 3, componentY + 3, 0)
				showImage(boardImage)
				


# first level shifter
shifterCoord = [85, 22]
shifterImage = cv2.imread('images/shifter.png', cv2.IMREAD_UNCHANGED)
boardImage = imageFuncs.insertImage(boardImage, shifterImage, shifterCoord[0], shifterCoord[1], 0)
showImage(boardImage)


def arduinoToShifter(pin1num, pin2num):
	boardCopy = boardImage.copy()
	pin1name = 'arduino' + str(pin1num)
	pin2name = 'shifter' + str(pin2num)
	newBoardImage = imageFuncs.highlightArduinoAndShifter(boardCopy, pin1name, pin2name, shifterCoord)
	showImage(newBoardImage)

def shifterToGround(pinnum):
	boardCopy = boardImage.copy()
	pinname = 'shifter' + str(pinnum)
	newBoardImage = imageFuncs.shifterToGround(boardCopy, pinname, shifterCoord)
	showImage(newBoardImage)

# first level shifter connections to Arduino
arduinoToShifter(30, 12)
arduinoToShifter(2, 11)
arduinoToShifter(9, 10)
arduinoToShifter(19, 8)

# first shifter to ground
#shifterToGround(1)

# lcd screen
lcdCoord = [116, 3]
lcdImage = cv2.imread('images/lcd.png', cv2.IMREAD_UNCHANGED)
boardImage = imageFuncs.insertImage(boardImage, lcdImage, lcdCoord[0], lcdCoord[1], 0)
showImage(boardImage)

def lcdToShifter(pin1num, pin2num):
	boardCopy = boardImage.copy()
	pin1name = 'lcd' + str(pin1num)
	pin2name = 'shifter' + str(pin2num)
	newBoardImage = imageFuncs.highlightLcdAndShifter(boardCopy, pin1name, pin2name, shifterCoord)
	showImage(newBoardImage)


lcdToShifter(3, 2)
lcdToShifter(4, 3)
lcdToShifter(5, 4)

# second level shifter
shifterCoord = [85, 37]
shifterImage = cv2.imread('images/shifter.png', cv2.IMREAD_UNCHANGED)
boardImage = imageFuncs.insertImage(boardImage, shifterImage, shifterCoord[0], shifterCoord[1], 0)
showImage(boardImage)

	
# second level shifter connections
arduinoToShifter(19, 14)
arduinoToShifter(8, 13)
arduinoToShifter(7, 12)
lcdToShifter(2, 6)
lcdToShifter(3, 7)
#shifterToGround(8)


# finishing touches
resistorImage = cv2.imread('images/resistor.png', cv2.IMREAD_UNCHANGED)
boardImage = imageFuncs.insertImage(boardImage, resistorImage, 112, 23, 90)
showImage(boardImage)


boardCopy = boardImage.copy()
boardCopy = imageFuncs.insertCircle(boardCopy, 10, 49, (255, 0, 255))
boardCopy = imageFuncs.insertCircle(boardCopy, 121, 52, (255, 0, 255))
boardCopy = imageFuncs.insertCircle(boardCopy, 112, 24, (255, 0, 255))
boardCopy = imageFuncs.insertCircle(boardCopy, 95, 38, (255, 0, 255))
boardCopy = imageFuncs.insertCircle(boardCopy, 95, 35, (255, 0, 255))
showImage(boardCopy)

boardCopy = boardImage.copy()
boardCopy = imageFuncs.insertCircle(boardCopy, 121, 24, (255, 0, 255))
boardCopy = imageFuncs.insertCircle(boardCopy, 114, 24, (255, 0, 255))
cv2.imwrite('output/image1.png', boardCopy)
showImage(boardCopy)


cv2.waitKey(0)
cv2.destroyAllWindows()




