import os
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
camera_type = 'picamera'
IM_WIDTH = 1280
IM_HEIGHT = 720
font = cv2.FONT_HERSHEY_PLAIN
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    frame = np.copy(frame1.array)
    frame.setflags(write=1)
    frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_expanded = np.expand_dims(frame_rgb,axis=0)
    decodeObjects = pyzbar.decode(frame)
    for obj in decodeObjects:
        print ("Data",obj.data)
        cv2.putText(frame, str(obj.data), (50,50), font, 2,(255,0,0),3)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1)== ord('q'):
        break
    rawCapture.truncate(0)

