import numpy as np
import cv2 as cv
import math
import datetime

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_250)
parameters= cv.aruco.DetectorParameters_create()

cap=cv.VideoCapture(0)

while (True):
    ret,frame=cap.read()
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    markerCorners,markerIds,rejectedCandidates=cv.aruco.detectMarkers(frame,dictionary,parameters=parameters)
    if markerIds is not None:
        for i,corner in zip(markerIds,markerCorners):
            print(corner[0][0][0],corner[0][1][1])
            print(i)
        frame=cv.aruco.drawDetectedMarkers(frame,markerCorners,borderColor=(0,255,0))
    cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()    
    