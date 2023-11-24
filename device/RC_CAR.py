import sys
sys.path.append('Raspi-MotorHAT-python3')

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM

# Configure DC Motor
mh = Raspi_MotorHAT(addr = 0x6F)
dcMotor = mh.getMotor(2) # pin
dcMotor.setSpeed(0) # speed

# Configure Servo Motor
servo = PWM(0x6F)
servo.setPWMFreq(60)

# RC Car class for driving
class rcCar:

    # car status
    FORWARD = 1
    BACKWARD = 2
    RELEASE = 3
    LEFT = 4
    RIGHT = 5
    STOP = 6
    OFF = 7
    
    def __init__(self, speed=0, direction=500, moveState=3, directionState=6):
        self.speed = speed
        self.direction = direction
        self.moveState = moveState
        self.directionState = directionState

    # set RC Car status according to command
    def setState(self, cmd):
        if(cmd == 'up_press' and self.moveState == self.RELEASE):
            self.moveState = self.FORWARD

        elif(cmd == 'down_press' and self.moveState == self.RELEASE):
            self.moveState = self.BACKWARD

        elif(cmd == 'left_press' and self.directionState == self.STOP):
            self.directionState = self.LEFT

        elif(cmd == 'right_press' and self.directionState == self.STOP):
            self.directionState = self.RIGHT

        elif(cmd == 'up_stop' and self.moveState == self.FORWARD):
            self.moveState = self.RELEASE

        elif(cmd == 'down_stop' and self.moveState == self.BACKWARD):
            self.moveState = self.RELEASE

        elif(cmd == 'left_stop' and self.directionState == self.LEFT):
            self.directionState = self.STOP

        elif(cmd == 'right_stop' and self.directionState == self.RIGHT):
            self.directionState = self.STOP
        
        elif(cmd == 'off'):
            self.moveState = self.OFF
            self.directionState = self.OFF
    
    # move forward
    def forward(self):
        if(self.speed >= 120):
            return

        self.speed += 10
        dcMotor.setSpeed(self.speed)
        dcMotor.run(Raspi_MotorHAT.BACKWARD)
    
    # move backward
    def backward(self):
        if(self.speed >= 120):
            return

        self.speed += 10
        dcMotor.setSpeed(self.speed)
        dcMotor.run(Raspi_MotorHAT.FORWARD)

    # turn left
    def left(self):
        if(self.direction <= 330):
            return

        self.direction -= 10
        servo.setPWM(0, 0, self.direction)
        
    # turn right
    def right(self):
        if(self.direction >= 570):
            return

        self.direction += 10
        servo.setPWM(0, 0, self.direction)

    # stop moving
    def moveStop(self):
        self.speed = 0
        dcMotor.setSpeed(self.speed)

    # quit running
    def quit(self):
        dcMotor.setSpeed(0)
        dcMotor.run(Raspi_MotorHAT.RELEASE)
        servo.setPWM(0, 0, 450)
