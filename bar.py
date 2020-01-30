import os
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

while True:
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
    x = input("wait for switch")
    if x == "B":
        camera.start_preview()
        time.sleep(2)
        camera.capture('qr.jpg')
        camera.close()
        image = cv2.imread('qr.jpg')
        boundaries = [
            ([17,15,100],[50,56,200]),
            ([86,31,4],[220,88,50]),
            ([25,146,190],[62,174,250]),
            ([103,86,65],[145,133,128])
            ]
        for (lower,upper)in boundaries:
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            
            mask = cv2.inRange(image , lower , upper)
            output = cv2.bitwise_and(image,image,mask = mask)
            
            cv2.imshow("image",np.hstack([image, output]))
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            
            
    if x == "A":
        camera.start_preview()
        time.sleep(2)
        camera.capture('qr.jpg')
        camera.close()
        image = cv2.imread('qr.jpg')
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            (x ,y  ,w ,h) = barcode.rect
            cv2.rectangle(image, (x,y),(x+w,y+h),(0,0,255),2)
        
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
        
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x,y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        
            print("[INFO] Found {} barcode: {}".format(barcodeType,barcodeData))
        cv2.imshow("Image",image)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    
    
    
    
# for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
#     frame = np.copy(frame1.array)
#     frame.setflags(write=1)
#     frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#     frame_expanded = np.expand_dims(frame_rgb,axis=0)
#     decodeObjects = pyzbar.decode(frame)
#     for obj in decodeObjects:
#         print ("Data",obj.data)
#         cv2.putText(frame, str(obj.data), (50,50), font, 2,(255,0,0),3)
#     cv2.imshow("Frame",frame)
#     if cv2.waitKey(1)== ord('q'):
#         break
#     rawCapture.truncate(0)

