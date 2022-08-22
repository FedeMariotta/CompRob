from tkinter.tix import Tree
from rplidar import RPLidar
import numpy as np
from math import floor
'''
lidar = RPLidar(PORT_NAME)
 
i = 0
angulo = 0
distmin = 200000
angmin = 0
for measurment in lidar.iter_measurments():
    print("a")
    if (i == 0):
        angulo = measurment[2]
        i = 1
    if (measurment[2] >= angulo-1 and i != 0 and measurment[2] < angulo):
        print("Termino una rondaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #lidar.stop()
        break
    if (measurment[3] < distmin and measurment[3] > 0):
        distmin = measurment[3]
        angmin  = measurment[2] 
    print(distmin) 
    print(angmin)
    lidar.stop()
'''


PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

#   Calucla la distancia correspondiente a cada grado y promedia mediciones
#   cantMaxVueltas := cantidad de vueltas que da el sensor tomando medidas paracalcular promedio
#   Retorna una lista donde la posicion corresponde al grado y el valor a la medida promedio en cm
def dist(cantMaxVueltas=1):
    posPrimerMedida=0 #posicion de la primer medicion
    cantVueltas=0 # cantidad de vueltas completas que dio el sensor
    distancias = np.zeros((360, 2), int) #Posicion es angulo, (cantMediciones, sumaDistancias)
    resultado= np.zeros(360, int) #Posicion es angulo, valor es distancia en centimetros
    
    try:
        lidar.clear_input()
        for scan in lidar.iter_scans():#Si no anda, asignar iter_measurments a una variable e iterarla en el for(Como el ej de iter_scans)
            grado=floor(scan[1])
            distancias[grado, 0]=distancias[grado, 0]+1
            distancias[grado, 1]= distancias[grado, 1]+scan[2]
            
            if(grado==((posPrimerMedida-1)%360)):#Puede dar problema si no hay medidas de un grado y justo es el requerido
                cantVueltas=cantVueltas+1
                if(cantVueltas>=(cantMaxVueltas)):
                    break
    except:
        lidar.reset()
        print("Error en LIDAR")
    print(distancias)
    for i in range(0, 360):
        if (distancias[i,0]!=0):
            resultado[i]=distancias[i, 1]/distancias[i, 0] #Suma total de distancias / cant de medidas que se tomaron por angulo
    return resultado

while(True):
    print("Nuevo llamado: ------------- ")
    resu=dist(1)
    print(resu)