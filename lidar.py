#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar


PORT_NAME = '/dev/ttyUSB0'



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
            a = 5
            distmin = measurment[3]
            angmin = measurment[2] 
        print(distmin) 
        print(angmin)
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()

