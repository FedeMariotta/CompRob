#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

while(True):
    #lidar.stop_motor()
    #lidar.stop()
    #lidar.disconnect()
    #lidar = RPLidar(PORT_NAME)    
    i = 0
    angulo = 0
    distmin = 200000
    angmin = 0
    print('Recording measurments... Press Crl+C to stop.')
    #iterador = lidar.iter_measurments()
    a = lidar.get_info()
    #lidar.clear_input()
    
    #lidar.disconnect()
    #lidar = RPLidar(PORT_NAME) 
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