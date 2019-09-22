
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

width = 1280
height = 720
FPS = 24
seconds = 10
radius = 150
paint_h = int(height/2)

fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./circle_noise.avi', fourcc, float(FPS), (width, height))

for paint_x in range(-radius, width+radius, 6):
    frame = np.random.randint(0, 256, 
                              (height, width, 3), 
                              dtype=np.uint8)
    cv2.circle(frame, (paint_x, paint_h), radius, (0, 0, 0), -1)
    video.write(frame)

video.release()