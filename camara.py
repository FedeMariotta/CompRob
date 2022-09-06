import cv2
import numpy as np
from Ax12 import Ax12
from rplidar import RPLidar
import time
import math
import os
import queue
import threading




os.system("sudo bash ./camara.sh")
anterior_x = 0
anterior_y = 0

valor_anterior = 180
valor_ant = 0

Ax12.DEVICENAME = '/dev/ttyUSB1' #motores


Ax12.BAUDRATE = 1_000_000

Ax12.connect()

sentido = "izquierda"
final = False
estado = 0
color_nuevo = 0
#0 = yendo a buscar cubo, 1 = alineando estanterias y acercandose a los colores del piso, 2 = buscar el color del piso, 3  = por si no encuentra color, 4 = deja el cubo y vuelve al medio

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

parada = [300, 350]
i = 0 

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(10, 15)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


def laser():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    try:
        lidar.connect()
        a = lidar.get_info()
        for measurment in lidar.iter_measurments():
            if (i == 0):
                angulo = measurment[2]
                i = 1
            if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
                break
            if (measurment[3] < distmin and measurment[3] > 0):
                distmin = measurment[3]
                angmin  = measurment[2] 
        lidar.stop()
    except:
        print("Error")
    return (distmin, angmin)

def laseratras():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    try:
        lidar.connect()
        a = lidar.get_info()
        for measurment in lidar.iter_measurments():
            if (i == 0):
                angulo = measurment[2]
                i = 1
            if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
                break
            if (measurment[3] < distmin and measurment[3] > 0 and measurment[2] > 165 and measurment[2] < 195):
                distmin = measurment[3]
                angmin  = measurment[2] 
        lidar.stop()
    except:
        print("Error lidar")
    return (distmin, angmin)

def laseradelante():
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    try:
        lidar.connect()
        a = lidar.get_info()
        for measurment in lidar.iter_measurments():
            if (i == 0):
                angulo = measurment[2]
                i = 1
            if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
                break
            if (measurment[3] < distmin and measurment[3] > 0 and (measurment[2] > 345 or measurment[2] < 15)):
                distmin = measurment[3]
                angmin  = measurment[2] 
        lidar.stop()
    except:
        print("Error lidar")
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
        return(17, 45, 0, 35, 255)
    elif (color == "verde"):
        return (30, 80, 20, 85, 255)
    elif (color == "azul"):
        return (95, 60, 55, 135, 255)
    elif (color == "rojo"):
        return (160, 100, 20, 179, 255)
    elif (color == "negro"):
        return (0, 0, 0, 180, 100)
    
def buscar_color(h_min, s_min, v_min, h_max, ultimo):
    global cap
    frame = cap.read()
    image =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('camara', frame)
    area = 0
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, 255, ultimo])
    mask = cv2.inRange(image, lower, upper)  
    result = cv2.bitwise_and(frame, frame, mask=mask)   
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
            print("Cambie a estado ", estado)
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
    global valor_ant
    while not(l[1] > 165 and l[1] < 195):
        if (l[1] < 180):
            izquierda(123)
        else:
            derecha(123)
        l1 = laser()
        print(l1[1])
        print(abs(l1[1] - valor_ant))
        if (abs(l1[1] - valor_ant) < 40 or abs(l1[1] - valor_ant) > 320) and l1[1] != 0:
            l = l1
            valor_ant = l1[1]
        print(l[0], l[1])
    if (estado != 3 and estado != 4):
        while not(l[0] > 1500 and l[0] <1600):
            print(l[0])
            if (l[1] < 180):
                izquierda(123)
            else:
                derecha(123)
            adelante(180)
            l = laseratras() 
        estado = 2
        print("Cambie a estado", estado)
        global i
        i = (i+1) % 2
    parar()

    
def estanterias_adelante():
    global valor_anterior
    parar()
    global estado
    l = laser()
    print(l[0], l[1])
    print("Estoy haciendo estanterias adelante")
    while (l[1] > 15 and l[1] < 345 or l[1] == 0):
        if (l[1] > 180):
            izquierda(123)
        else:
            derecha(123)
        l1 = laser()
        if abs(l1[1] - valor_anterior) < 40:
            l = l1
            valor_anterior = l1[1]
        print(l[0], l[1])
    
    while not(l[0] > 1700 and l[0] < 1800):
        if (l[1] > 180):
            izquierda(123)
        else:
            derecha(123)
        if (l[0] > 1800):    
            adelante(180)
        elif (l[0] < 1500):
            atras(120)
        l = laseradelante()   
    estado = 0
    print("Cambie a estado", estado)
    global i
    i = (i+1) % 2
    parar()
    print("Termine")

cap = VideoCapture(-1)

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
            print(color)
            go_to_goal(x, y, 1)   
        
    elif (estado == 1):
        adelante(170)
        time.sleep(3)
        estanterias_atras()
        
    elif (estado == 2): #dejamos el cubo en el color correcto
        if (color == "rojo"):
            ar = devolver_tupla("rojo")
            x_red, y_red, aa = buscar_color(0, 100, 20, 10, 255) 
            if (x_red == 0 and y_red == 0):
                atras(100)
                print("Cambie a estado", estado)
            else:
                go_to_goal(x_red, y_red, 4) 
        elif (color == "verde"):
            av = devolver_tupla("verde")
            x_green, y_green, av = buscar_color(av[0], av[1], av[2], av[3], av[4]) 
            if (x_green == 0 and y_green == 0):
                atras(100)
                print("Cambie a estado", estado)
            else:
                go_to_goal(x_green, y_green, 4)
        elif (color == "azul"):
            az = devolver_tupla("azul")
            x_blue, y_blue, aa = buscar_color(az[0], az[1], az[2], az[3], az[4]) 
            if (x_blue == 0 and y_blue == 0):
                atras(100)
                print("Cambie a estado", estado)
            else:
                go_to_goal(x_blue, y_blue, 4)
        elif (color == "amarillo"):
            aa = devolver_tupla("amarillo")
            x_yellow, y_yellow, aa = buscar_color(aa[0], aa[1], aa[2], aa[3], aa[4]) 
            if (x_yellow == 0 and y_yellow == 0):
                atras(100)
                print("Cambie a estado", estado)
            else:
                go_to_goal(x_yellow, y_yellow, 4)
                
    elif (estado == 3):
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
            n = devolver_tupla("negro")
            x_black, y_black, a = buscar_color(n[0], n[1], n[2], n[3], n[4])
            adelante(170)
         
            
        
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
        estado = 2 #vuelvo a chequear el color
        print("Cambie a estado", estado)
    elif (estado == 4):
        parar()
        #deberia dejar el cubo
        #deja el cubo
        adelante(123)
        time.sleep(2)
        print("Deje el cubo")
        atras(170)
        time.sleep(5)
        estanterias_adelante()
        estado = 0        
    #se alinea con las estanterias al frente

    
            
cap.release()
cv2.destroyAllWindows()
