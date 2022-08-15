from Ax12 import Ax12

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB1'

Ax12.BAUDRATE = 1_000_000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id_der = 1
my_dxl_der = Ax12(motor_id_der)

motor_id_izq = 2
my_dxl_izq = Ax12(motor_id_izq)  

my_dxl_der.set_moving_speed(0)
my_dxl_izq.set_moving_speed(0)
