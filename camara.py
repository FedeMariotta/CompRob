import cv2
import numpy as np
from Ax12 import Ax12
from rplidar import RPLidar
import time
import math
import os

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
#PORT_NAME = '/dev/ttyUSB0' #lidar

os.system("sudo bash ./camara.sh")
anterior_x = 0
anterior_y = 0
cap = cv2.VideoCapture(-1)
cap.set(10,15)

Ax12.DEVICENAME = '/dev/ttyUSB0' #motores


Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()

sentido = "izquierda"
final = False
estado = 0
color_nuevo = 0
#0 = yendo a buscar cubo, 1 = alineando estanterias y acercandose a los colores del piso, 2 = buscar el color del piso

PORT_NAME = '/dev/ttyUSB1'
lidar = RPLidar(PORT_NAME)

# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

parada = [300, 350]
i = 0 #cambiar a 0 despues!!!

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

def laser():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    #iterador = lidar.iter_measurments()
    try:
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
    except:
        print("Error")
        #lidar.disconnect()
        #lidar = RPLidar(PORT_NAME)
        #estanterias_atras()
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
        #return(17, 17, 60, 25, 255)
        return(17, 45, 0, 35, 255) #aca tengo que volver
    elif (color == "verde"):
        #return(35, 80, 20, 85, 255)
        return (30, 80, 20, 85, 255)
    elif (color == "azul"):
        return (95, 60, 55, 135, 255)
    elif (color == "rojo"):
        return (160, 100, 20, 179, 255)
    elif (color == "negro"):
        return (0, 0, 0, 180, 100)
    
def buscar_color(h_min, s_min, v_min, h_max, ultimo):
    global cap
    ret, frame = cap.read()
    image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('camara', frame)
    area = 0
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, 255, ultimo])
    mask = cv2.inRange(image, lower, upper)  
    result = cv2.bitwise_and(frame, frame, mask=mask)   
    if (h_min == 160):
        cv2.imshow('rojo', result)
    kernel = np.ones((2,2),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
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
    print("Y: ")
    print(y)
    print("X: ")
    print(x)
    if (y > parada[i]):
        if not(325 < x and x < 375):
            if (x < 350):
                izquierda(100)
            else:
                derecha(100)
        else:
            parar()
            time.sleep(0.5)
            global estado  
            estado = est
    else:
        if (not(corrigiendo) and 275 < x and x < 425):
            adelante(180)
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
    
    while not(l[1] > 165 and l[1] < 195):
        if (l[1] < 180):
            izquierda(123)
        else:
            derecha(123)
        l = laser()
    if (estado != 3 and estado != 4):
        while not(l[0] > 1500 and l[0] <1600):
            if (l[1] < 180):
                izquierda(123)
            else:
                derecha(123)
           # f(l[0])
            adelante(180)
            l = laseratras()  
        #print("ya me aleje lo suficiente") 
        #print(l[0])    
        estado = 2
        global i
        i = (i+1) % 2
    parar()

    
def estanterias_adelante():
    global estado
    l = laser()
    print("Estoy haciendo estanterias adelante")
    while (l[1] > 15 and l[1] < 345):
        if (l[1] > 180):
            izquierda(123)
        else:
            derecha(123)
        l = laser()
    print("Termine")
    if (estado != 4):
        while not(l[0] > 1600 and l[0] < 1700):
            adelante(180)
            l = laseratras()   
            estado = 2
            global i
            i = (i+1) % 2
    parar()
    
    
def pedir_imagen():
 
    ret, frame = cap.read()
    cv2.imshow('pr', frame)
    return frame



while (True):
    if (estado == 0):
        r = devolver_tupla("rojo")
        x_red, y_red, a = buscar_color(r[0], r[1], r[2], r[3], r[4])
        if (x_red == 0):
            x_red, y_red, a = buscar_color(0, 100, 20, 10, 255)
        v = devolver_tupla("verde")
        x_green, y_green, av = buscar_color(v[0], v[1], v[2], v[3], v[4])
        if y_green > 450:
          y_green = 0
          x_green = 0
        az = devolver_tupla("azul")
        x_blue, y_blue, a = buscar_color (az[0], az[1], az[2], az[3], az[4])
        am = devolver_tupla("amarillo")
        x_yellow, y_yellow, aa = buscar_color(am[0], am[1], am[2], am[3], am[4])
        
          
        if (math.sqrt(pow(x_yellow - x_green, 2)+pow(y_yellow - y_green, 2))) < 100:
            if (aa < av):
                x_yellow = 0
                y_yellow = 0
            else:
                x_green = 0
                y_green = 0
        
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
        
        if (cv2.waitKey(1) == ord('s')):
            break          
        if (y_red == 0 and y_yellow == 0 and y_green == 0 and y_blue == 0):
            #print("hola")
            adelante(100)
        else:
            #print(color)
            print(x, y)
            go_to_goal(x, y, 1)   
        
    elif (estado == 1):
        estanterias_atras()
        
    elif (estado == 2): #dejamos el cubo en el color correcto
        print("estado2")
        ar = devolver_tupla("rojo")
        x_red, y_red, aa = buscar_color(0, 100, 20, 10, 255)  
        if (anterior_x == 0 and anterior_y == 0):
            anterior_x = x_red
            anterior_y = y_red
        else:
            #if (abs(x_red-anterior_x) < 50 and abs(y_red-anterior_y) < 50):
            #    anterior_x = x_red
            #    anterior_y = y_red
            if (x_red == 0 and y_red == 0):
                    #print("if")
                estado = 3
            else:
                    #print("else")
                go_to_goal(x_red, y_red, 4)
        print("rojo")
        print(x_red, y_red)        
                
        
        
        '''
        r = devolver_tupla("rojo")
        x_red, y_red, a = buscar_color(r[0], r[1], r[2], r[3], frame, r[4])
        v = devolver_tupla("verde")
        x_green, y_green, av = buscar_color(v[0], v[1], v[2], v[3] ,frame, v[4])
        az = devolver_tupla("azul")
        x_blue, y_blue, a = buscar_color (az[0], az[1], az[2], az[3], frame, az[4])
        am = devolver_tupla("amarillo")
        x_yellow, y_yellow, aa = buscar_color(am[0], am[1], am[2], am[3], frame, am[4])  
        
        #print("Area amarilla")
        #print(aa)
        #print("Area verde")
        #print(av)
        
        if (math.sqrt(pow(x_yellow - x_green, 2)+pow(y_yellow - y_green, 2))) < 250:
            if (aa < av):
                x_yellow = 0
                y_yellow = 0
            else:
                x_green = 0
                y_green = 0
        
        #print(x_green, y_green, "verde")
        #print(x_yellow, y_yellow, "amarillo")  
         
        #me quedo con el y mas grande
        
        if (y_yellow > y_blue):
            if (y_yellow > y_green):
                if (y_yellow > y_red):
                    y = y_yellow
                    x = x_yellow
                    color_nuevo = "amarillo"
                else:
                    y = y_red
                    x = x_red
                    color_nuevo = "rojo"
            else:
                if (y_red > y_green):
                    y = y_red
                    x = x_red
                    color_nuevo = "rojo"
                else:
                    y = y_green
                    x = x_green
                    color_nuevo = "verde"
        else:
            if (y_blue > y_green):
                if (y_blue > y_red):
                    y = y_blue
                    x = x_blue
                    color_nuevo = "azul"
                else:
                    y = y_red
                    x = x_red
                    color_nuevo = "rojo"
            else:
                if (y_red > y_green):
                    y = y_red
                    x = x_red
                    color_nuevo = "rojo"
                else:
                    y = y_green
                    x = x_green
                    color_nuevo = "verde" 
        #print("El valor de y es:")
        #print(y)
        #print("El color es:")
        #print(color_nuevo)
        if (y == 0):
            adelante(100)
        else:
            go_to_goal(x, y, 3)#cmabiamos estado 3
    
        #print("estado2 pasa al 3")
        
        print(color)
        t = devolver_tupla(color)
        print(t[0])
        x, y, a = buscar_color(t[0], t[1], t[2], t[3], frame, t[4])
        print(x, y)
        if (y == 0):
            atras(100)
        else:
            go_to_goal(x, y, 4)
        '''
        
    elif (estado == 3):
        '''
        cv2.destroyAllWindows()
        frame = pedir_imagen()
        image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('camara', frame)
        print("estado3")
        print("El color que agarre es:")
        print(color)
        print("El color que estoy viendo es:")
        print(color_nuevo)
        if (color == color_nuevo):
            print("Colores coinciden")
            #dejo el cubo
            
            #cv2.imshow('camara', frame)
            tupla = devolver_tupla(color_nuevo)
            x, y, a = buscar_color(tupla[0], tupla[1], tupla[2], tupla[3], frame, tupla[4])
            
            print("Las coordenadas son")
            print(x, y)
            print("i")
            print(i)
            go_to_goal(x, y, 4)
            #parar()
            #time.sleep(1)
        else:
        '''
            #print("Ahora")
            #time.sleep(2)
            #estanterias_atras()
            #parar()
        if (sentido == "izquierda"):
            izquierda(123)
        else:
            derecha(123)
        a = (53/10)
        time.sleep(53/10)
        print("Gire a buscar otro color")
        
            
        
        n = devolver_tupla("negro")
        x_black, y_black, a = buscar_color(n[0], n[1], n[2], n[3], n[4]) 
        
        print("coordenadas negro")
        print(x_black, y_black)
        
        #chequear que no se salga
        ahora = time.time()
        while(x_black != 0 and y_black != 0 and time.time()-ahora < 6):
            print("avanzo")
            frame = pedir_imagen()
            image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            n = devolver_tupla("negro")
            x_black, y_black, a = buscar_color(n[0], n[1], n[2], n[3], n[4])
            adelante(170)
            #cv2.circle(frame, (x_black,y_black), 7, (255,255,255), -1)  
            #cv2.imshow('camara', frame)       
            
        
        if (x_black == 0 or y_black == 0): #sali porque no veo negro, tengo que ir para el otro lado
            if (sentido == "izquierda"):
                sentido = "derecha"
            else:
                sentido = "izquierda"
       
            derecha(123)
            time.sleep(18) #180 grados, doy vuelta el sentido
            print("gire 180")
        
        if (sentido == "izquierda"):
            derecha(123)
        else:
            izquierda(123)
        print("Estoy girandooooooo")
        time.sleep(53/10)
        print("Termine de girar")
        #print("estoy viendo color")
        #atras(100)
        #time.sleep(1)
        estado = 2 #vuelvo a chequear el color
    elif (estado == 4):
        print("estado4")
        estanterias_atras() #lo enderezamos
        parar()
        #deberia dejar el cubo
        #deja el cubo
        print("Deje el cubo")
        atras(170)
        time.sleep(3)
        estanterias_adelante()
        estado = 0        
    #se alinea con las estanterias al frente
    #cv2.imshow('verde', result_green)
    #cv2.imshow('rojo', result_red)
    
    
    
    #cv2.imshow('mask', lower_mask)
    #cv2.imshow('result', result)
         
    
            
cap.release()
cv2.destroyAllWindows()
