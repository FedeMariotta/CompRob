import cv2
import numpy as np
from Ax12 import Ax12

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

def izquierda(vel):
    my_dxl_der.set_moving_speed(1023+vel)
    my_dxl_izq.set_moving_speed(1023+vel)

def derecha(vel):
    my_dxl_der.set_moving_speed(vel)
    my_dxl_izq.set_moving_speed(vel)
    
def adelante(vel):
    my_dxl_der.set_moving_speed(1023+vel)
    my_dxl_izq.set_moving_speed(vel)
    
def atras(vel):
    my_dxl_der.set_moving_speed(vel)
    my_dxl_izq.set_moving_speed(1023+vel)

def parar():
    my_dxl_der.set_moving_speed(0)
    my_dxl_izq.set_moving_speed(0)


corrigiendo = False
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
    
    #go to goal
    if (not(corrigiendo) and -0.35 < y and y < 0.35):
        adelante(123)
    else:
        corrigiendo = True
        if (y < 0):
            derecha(307)
        else:
            izquierda(307)
        corrigiendo = False
    
    cv2.circle(frame, (x,y), 7, (255,0,0), -1)
    cv2.imshow('prueba2', result)
    cv2.imshow('prueba', frame)
    
    #cv2.imshow('mask', lower_mask)
    #cv2.imshow('result', result)
    
    if (cv2.waitKey(1) == ord('s')):
        break
            
cap.release()
cv2.destroyAllWindows()
