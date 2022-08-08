import cv2
import numpy as np
cap = cv2.VideoCapture(-1)

while (True):
    ret, frame = cap.read()

    image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([160,100,20])
    upper = np.array([179,255,255])
    lower_mask = cv2.inRange(image,lower,upper)
    
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    kernel = np.ones((2,2),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    #result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(big_contour)
    if (M["m00"]==0): M["m00"]=1
    x = int(M["m10"]/M["m00"])
    y = int(M["m01"]/M["m00"])
    cv2.circle(frame, (x,y), 7, (255,0,0), -1)
    cv2.imshow('prueba2', result)
    cv2.imshow('prueba', frame)
    
    #cv2.imshow('mask', lower_mask)
    #cv2.imshow('result', result)
    
    if (cv2.waitKey(1) == ord('s')):
        break
            
cap.release()
cv2.destroyAllWindows()
