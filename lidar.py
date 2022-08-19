from rplidar import RPLidar
import numpy as np
from math import floor
PORT_NAME = '/dev/ttyUSB0'
#lidar = RPLidar(PORT_NAME)
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
medidasTomadas=[]

#   Calucla la distancia correspondiente a cada grado y promedia mediciones
#   cantMaxVueltas := cantidad de vueltas que da el sensor tomando medidas paracalcular promedio
#   Retorna una lista donde la posicion corresponde al grado y el valor a la medida promedio en cm
def dist(cantMaxVueltas=1):
    posPrimerMedida=0 #posicion de la primer medicion
    cantVueltas=0 # cantidad de vueltas completas que dio el sensor
    distancias = np.zeros(360, 2) #Posicion es angulo, (cantMediciones, sumaDistancias)
    resultado= np.zeros(360) #Posicion es angulo, valor es distancia en centimetros
    
    try:
        #lidar.clear_input()
        for scan in medidasTomadas:
            cantMedActuales=distancias[floor(scan[1])][0]
            sumaMedActual=distancias[floor(scan[1])][1]
            distancias[floor(scan[1])]=(cantMedActuales+1, sumaMedActual+(scan[2]))

            if(floor(scan[1])==((posPrimerMedida-1)%360) or floor(scan[1])==posPrimerMedida):
                if(cantVueltas>=(cantMaxVueltas-1)):
                    break
                cantVueltas=cantVueltas+1
    except:
        #lidar.reset()
        print("Error en LIDAR")

    for i in distancias:
        if (i[0]==0):
            resultado[i]=0
        else:
            resultado[i]=distancias[i][1]/distancias[i][0] #Suma total de distancias / cant de medidas que se tomaron por angulo
    return distancias

for i in range(0, 360):
    medidasTomadas.apend((i,i,1))
resu=dist()
print(resu)