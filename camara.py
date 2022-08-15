import cv2
import numpy as np
from Ax12 import Ax12
from rplidar import RPLidar

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
PORT_NAME = '/dev/ttyUSB0' #lidar

Ax12.DEVICENAME = '/dev/ttyUSB1' #motores

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()



# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

def laser():
    lidar = RPLidar(PORT_NAME)
    angulo = 0
    i = 0
    distmin = 200000
    angmin = 0
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measurments():
            if (i == 0):
                angulo = measurment[2]
                i = 1
            if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
                break
            if (measurment[3] < distmin and measurment[3] > 0):
                distmin = measurment[3]
                angmin = measurment[2] 
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    return (distmin, angmin)
    
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
     #enderezarnos
    l = laser()
    while not(l[1] > 175 and l[1] < 185):
        print(l[1])
        if (l[1] < 180):
            derecha(123)
        else:
            izquierda(123)
        l = laser()
    parar()   

    '''
    ret, frame = cap.read()

    image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([160,100,20])
    upper_red = np.array([179,255,255])
    
    lower_green = np.array([40,80,20])
    upper_green = np.array([80,255,255])
    
    lower_blue = np.array([100,80,2])
    upper_blue = np.array([126,255,255])
    
    lower_yellow = np.array([22,70,0])
    upper_yellow = np.array([50,255,255])
    
    lower_mask_red = cv2.inRange(image,lower_red,upper_red)
    
    lower_mask_green = cv2.inRange(image, lower_green, upper_green)
    
    lower_mask_blue = cv2.inRange(image, lower_blue, upper_blue)
    
    lower_mask_yellow = cv2.inRange(image, lower_yellow, upper_yellow)
    
    mask_red = cv2.inRange(image, lower_red, upper_red)
    
    mask_green = cv2.inRange(image, lower_green, upper_green)
    
    mask_blue = cv2.inRange(image, lower_blue, upper_blue)
    
    mask_yellow = cv2.inRange(image, lower_yellow, upper_yellow)
    
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    
    result_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    
    result_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    
    kernel = np.ones((2,2),np.uint8)
    result_red = cv2.morphologyEx(result_red, cv2.MORPH_OPEN, kernel)
    
    result_green = cv2.morphologyEx(result_green, cv2.MORPH_OPEN, kernel)
    
    result_blue = cv2.morphologyEx(result_blue, cv2.MORPH_OPEN, kernel)
    
    result_yellow = cv2.morphologyEx(result_yellow, cv2.MORPH_OPEN, kernel)
    #result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    
    contours_red,_ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_green,_ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_blue,_ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_yellow,_ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if (len(contours_red) == 0):
        x_red = 0
        y_red = 0
    else:
        big_contour_red = max(contours_red, key=cv2.contourArea)    
        M_red = cv2.moments(big_contour_red)
        if (M_red["m00"]==0): M_red["m00"]=1
        x_red = int(M_red["m10"]/M_red["m00"])
        y_red = int(M_red["m01"]/M_red["m00"])
        
    if(len(contours_green) == 0):
        x_green = 0
        y_green = 0
    else:
        big_contour_green = max(contours_green, key=cv2.contourArea)    
        M_green = cv2.moments(big_contour_green)
        if (M_green["m00"]==0): M_green["m00"]=1
        x_green = int(M_green["m10"]/M_green["m00"])
        y_green = int(M_green["m01"]/M_green["m00"])
    if (len(contours_blue) == 0):
        x_blue = 0
        y_blue = 0
    else:    
        big_contour_blue = max(contours_blue, key=cv2.contourArea)    
        M_blue = cv2.moments(big_contour_blue)
        if (M_blue["m00"]==0): M_blue["m00"]=1
        x_blue = int(M_blue["m10"]/M_blue["m00"])
        y_blue = int(M_blue["m01"]/M_blue["m00"])
    if (len(contours_yellow) == 0):
        x_yellow = 0
        y_yellow = 0
    else:    
        big_contour_yellow = max(contours_yellow, key=cv2.contourArea)
        M_yellow = cv2.moments(big_contour_yellow)    
        if (M_yellow["m00"]==0): M_yellow["m00"]=1
        x_yellow = int(M_yellow["m10"]/M_yellow["m00"])
        y_yellow = int(M_yellow["m01"]/M_yellow["m00"])
     
    #me quedo con el y mas grande
    
    if (y_yellow > y_blue):
        if (y_yellow > y_green):
            if (y_yellow > y_red):
                y = y_yellow
                x = x_yellow
            else:
                y = y_red
                x = x_red
        else:
            if (y_red > y_green):
                y = y_red
                x = x_red
            else:
                y = y_green
                x = x_green
    else:
        if (y_blue > y_green):
            if (y_blue > y_red):
                y = y_blue
                x = x_blue
            else:
                y = y_red
                x = x_red
        else:
            if (y_red > y_green):
                y = y_red
                x = x_red
            else:
                y = y_green
                x = x_green    
    
    #go to goal
    if (y > 380):
        if (325 < x and x < 375):
            a=5
        else:
            if (x < 350):
                izquierda(100)
            else:
                derecha(100)
        
        
        parar()
    else:
        if (not(corrigiendo) and 275 < x and x < 425):
            adelante(123)
        else:
            corrigiendo = True
            if (x < 350):
                izquierda(123)
            else:
                derecha(123)
            corrigiendo = False
        
    print("Recogi el cubo)
    
    cv2.circle(frame, (x_yellow,y_yellow), 7, (0,255,255), -1)
    cv2.circle(frame, (x_red,y_red), 7, (0,0,255), -1)
    cv2.circle(frame, (x_green,y_green), 7, (0,255,0), -1)
    cv2.circle(frame, (x_blue,y_blue), 7, (255,0,0), -1)
    
    cv2.imshow('amarillo', result_yellow)
    cv2.imshow('azul', result_blue)    
    cv2.imshow('verde', result_green)
    cv2.imshow('rojo', result_red)
    cv2.imshow('prueba', frame)
    '''   
    
   
    
    
    #cv2.imshow('mask', lower_mask)
    #cv2.imshow('result', result)
    
    if (cv2.waitKey(1) == ord('s')):
        break
            
cap.release()
cv2.destroyAllWindows()
