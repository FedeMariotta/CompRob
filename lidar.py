#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar


PORT_NAME = '/dev/ttyUSB0'



lidar = RPLidar(PORT_NAME)
try:
    print('Recording measurments... Press Crl+C to stop.')
    for measurment in lidar.iter_measurments():
        print(measurment)
except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
outfile.close()

