import os
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
import time
import pandas as pd
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
        img = cv2.imread('qr.jpg')
        clicked = False
        r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
        index=["color","color_name","hex","R","G","B"]
        csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
        def getColorName(R,G,B):
            minimum = 10000
            for i in range(len(csv)):
                d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
                if(d<=minimum):
                    minimum = d
                    cname = csv.loc[i,"color_name"]
            return cname

#function to get x,y coordinates of mouse double click
        def draw_function(event, x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                global b,g,r,xpos,ypos, clicked
                clicked = True
                xpos = x
                ypos = y
                b,g,r = img[y,x]
                b = int(b)
                g = int(g)
                r = int(r)
       
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_function)

        while(1):

            cv2.imshow("image",img)
            if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
                cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
                text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
                cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
                if(r+g+b>=600):
                    cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
                clicked=False

    #Break the loop when user hits 'esc' key    
            if cv2.waitKey(20) & 0xFF ==27:
                break
    
        cv2.destroyAllWindows()
            
            
    if x == "A":
#         for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
#             frame = np.copy(frame1.array)
#             frame.setflags(write=1)
#             frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#             frame_expanded = np.expand_dims(frame_rgb,axis=0)
#             decodeObjects = pyzbar.decode(frame)
#             for obj in decodeObjects:
#                 print ("Data",obj.data)
#                 cv2.putText(frame, str(obj.data), (50,50), font, 2,(255,0,0),3)
#             cv2.imshow("Frame",frame)
#             if cv2.waitKey(1)== ord('q'):
#                 cv2.destroyAllWindows()
#                 break
#             rawCapture.truncate(0)
        
        
        
        
        
        
        
        
        
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
        cv2.waitKey(0)
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

