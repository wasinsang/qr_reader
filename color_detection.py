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
    image = frame
    boundaries = [
        ([17,5,100],[50,56,200]),
        ([86,31,4],[220,88,50]),
        ([25,146,190],[62,174,250]),
        ([103,86,65],[145,133,128])
        ]
    for (lower,upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(lower, dtype = "uint8")
        
        mask = cv2.imRange(image, lower, upper)
        output = cv2.bitwise_and(image ,image, mask = mask)
    
        cv2.imshow("images",np.hstack([image,output]))
    if cv2.waitKey(1)== ord('q'):
        break
    rawCapture.truncate(0)


