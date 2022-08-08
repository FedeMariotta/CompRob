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





def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main(motor_object):
    """ sets goal position based on user input """
    bool_test = True
    while bool_test:

        print("\nPosition of dxl ID: %d is %d " %
              (motor_object.id, motor_object.get_present_position()))
        # desired angle input
        input_pos = int(input("goal pos: "))
        motor_object.set_goal_position(input_pos)
        print("Position of dxl ID: %d is now: %d " %
              (motor_object.id, motor_object.get_present_position()))
        bool_test = user_input()

# pass in AX12 object
main(my_dxl)

# disconnect
my_dxl.set_torque_enable(0)
Ax12.disconnect()
