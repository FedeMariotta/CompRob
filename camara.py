import cv2
import numpy as np
from Ax12 import Ax12
from rplidar import RPLidar
import time
import math

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
#PORT_NAME = '/dev/ttyUSB0' #lidar

Ax12.DEVICENAME = '/dev/ttyUSB1' #motores


Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()

estado = 0
#0 = yendo a buscar cubo, 1 = alineando estanterias y acercandose a los colores del piso, 2 = buscar el color del piso

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

parada = [380, 325]
i = 0 #cambiar a 0 despues!!!

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

def laser():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    #iterador = lidar.iter_measurments()
    a = lidar.get_info()
    #lidar.clear_input()
    
    #lidar.disconnect()
    #lidar = RPLidar(PORT_NAME) 
    for measurment in lidar.iter_measurments():
        if (i == 0):
            angulo = measurment[2]
            i = 1
        if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
            #lidar.stop()
            break
        if (measurment[3] < distmin and measurment[3] > 0):
            distmin = measurment[3]
            angmin  = measurment[2] 
    lidar.stop()
    return (distmin, angmin)

def laseratras():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    #iterador = lidar.iter_measurments()
    a = lidar.get_info()
    #lidar.clear_input()
    
    #lidar.disconnect()
    #lidar = RPLidar(PORT_NAME) 
    for measurment in lidar.iter_measurments():
        if (i == 0):
            angulo = measurment[2]
            i = 1
        if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
            #lidar.stop()
            break
        if (measurment[3] < distmin and measurment[3] > 0 and measurment[2] > 165 and measurment[2] < 195):
            distmin = measurment[3]
            angmin  = measurment[2] 
    lidar.stop()
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
    
def devolver_tupla(color):
    if (color == "amarillo"):
        return(17, 45, 0, 55)
    elif (color == "verde"):
        return (30, 80, 20, 85)
    elif (color == "azul"):
        return (100, 80, 2, 126)
    elif (color == "rojo"):
        return (160, 100, 20, 179)
    
def buscar_color(h_min, s_min, v_min, h_max, frame):
    area = 0
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, 255, 255])
    mask = cv2.inRange(image, lower, upper)  
    result = cv2.bitwise_and(frame, frame, mask=mask)   
    kernel = np.ones((2,2),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('colores', result)
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
    if (len(contours) == 0):    
        x = 0
        y = 0
    else:
        big_contour = max(contours, key=cv2.contourArea)  
        area = cv2.contourArea(big_contour) 
        if (cv2.contourArea(big_contour) > 350):
            M = cv2.moments(big_contour)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
        else:
            x = 0
            y = 0        
    return (x,y, area)
    

        
def go_to_goal(x, y, est):
    corrigiendo = False
    if (y > parada[i]):
        if not(325 < x and x < 375):
            if (x < 350):
                izquierda(100)
            else:
                derecha(100)
        parar()
        time.sleep(0.5)
        global estado
        estado = est
    else:
        if (not(corrigiendo) and 275 < x and x < 425):
            adelante(170)
        else:
            corrigiendo = True
            if (x < 350):
                izquierda(123)
            else:
                derecha(123)
            corrigiendo = False
            
def estanterias_atras():
    global estado
    l = laser()
    try:
        while not(l[1] > 165 and l[1] < 195):
            if (l[1] < 180):
                izquierda(123)
            else:
                derecha(123)
            l = laser()
        if (estado != 3):
            while not(l[0] > 1800 and l[0] < 1900):
                print(l[0])
                adelante(170)
                l = laseratras()   
                estado = 2
                global i
                i = (i+1) % 2
        parar()
    except:
        l.disconnect()
        lidar = RPLidar(PORT_NAME)
        estanterias_atras()
    
def estanterias_adelante():
    global estado
    l = laser()
    while (l[1] > 15 and l[1] < 345):
        if (l[1] > 180):
            izquierda(123)
        else:
            derecha(123)
        l = laser()
    if (estado != 3):
        while not(l[0] > 2000 and l[0] < 2100):
            adelante(170)
            l = laseratras()   
            estado = 2
            i = (i+1) % 2
    parar()
    

cap = cv2.VideoCapture(-1)

while (True):
    cap.set(10,15)
    ret, frame = cap.read()
    image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if (estado == 0):
        #ret, frame = cap.read()
    
 #       image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        r = devolver_tupla("rojo")
        x_red, y_red, a = buscar_color(r[0], r[1], r[2], r[3], frame)
        v = devolver_tupla("verde")
        x_green, y_green, av = buscar_color(v[0], v[1], v[2], v[3] ,frame)
        az = devolver_tupla("azul")
        x_blue, y_blue, a = buscar_color (az[0], az[1], az[2], az[3], frame)
        am = devolver_tupla("amarillo")
        x_yellow, y_yellow, aa = buscar_color(am[0], am[1], am[2], am[3], frame)  
        
        if (math.sqrt(pow(x_yellow - x_green, 2)+pow(x_yellow - x_green, 2))) < 250:
            if (aa < av):
                x_yellow = 0
                y_yellow = 0
            else:
                x_green = 0
                y_green = 0
        
        print(x_green, y_green, "verde")
        print(x_yellow, y_yellow, "amarillo")  
         
        #me quedo con el y mas grande
        
        if (y_yellow > y_blue):
            if (y_yellow > y_green):
                if (y_yellow > y_red):
                    y = y_yellow
                    x = x_yellow
                    color = "amarillo"
                else:
                    y = y_red
                    x = x_red
                    color = "rojo"
            else:
                if (y_red > y_green):
                    y = y_red
                    x = x_red
                    color = "rojo"
                else:
                    y = y_green
                    x = x_green
                    color = "verde"
        else:
            if (y_blue > y_green):
                if (y_blue > y_red):
                    y = y_blue
                    x = x_blue
                    color = "azul"
                else:
                    y = y_red
                    x = x_red
                    color = "rojo"
            else:
                if (y_red > y_green):
                    y = y_red
                    x = x_red
                    color = "rojo"
                else:
                    y = y_green
                    x = x_green
                    color = "verde" 
        cv2.circle(frame, (x_yellow,y_yellow), 7, (0,255,255), -1)
        cv2.circle(frame, (x_red,y_red), 7, (0,0,255), -1)
        cv2.circle(frame, (x_green,y_green), 7, (0,255,0), -1)
        cv2.circle(frame, (x_blue,y_blue), 7, (255,0,0), -1)
        
        #cv2.imshow('prueba', frame) 
        
        if (cv2.waitKey(1) == ord('s')):
            break          
        if (y_red == 0 and y_yellow == 0 and y_green == 0 and y_blue == 0):
            adelante(170)
        else:
            #go to goal
            go_to_goal(x, y, 1)   
            print(color)   
            print("Agarre el cubo")
    
    elif (estado == 1):
        #enderezarnos
        estanterias_atras()
        print("estanterias atras")
        
    elif (estado == 2): #dejamos el cubo en el color correcto
        t_color = devolver_tupla(color)
        x, y, a = buscar_color(t_color[0], t_color[1], t_color[2], t_color[3], frame)
        if (x == 0 and y == 0):
            avanzar(100)
        #que pasa si no hay color?
        go_to_goal(x, y, 3)
    
    elif (estado == 3):
        estanterias_atras() #lo enderezamos
        parar()
        #deberia dejar el cubo
        atras(170)
        time.sleep(2)
        estanterias_adelante()
        estado = 0        
    #se alinea con las estanterias al frente
    #cv2.imshow('verde', result_green)
    #cv2.imshow('rojo', result_red)
    
   
    cv2.imshow('camara', frame)
    
    #cv2.imshow('mask', lower_mask)
    #cv2.imshow('result', result)
    
    
            
cap.release()
cv2.destroyAllWindows()
