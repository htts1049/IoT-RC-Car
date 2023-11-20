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
    
    def __init__(self, speed=0, direction=500, moveState=3, directionState=6):
        self.speed = speed
        self.direction = direction
        self.moveState = moveState
        self.directionState = directionState

    # set RC Car status according to command
    def setState(self, cmd):
        if(cmd == 'up' and self.moveState == self.RELEASE):
            self.moveState = self.FORWARD

        elif(cmd == 'down' and self.moveState == self.RELEASE):
            self.moveState = self.BACKWARD

        elif(cmd == 'left' and self.directionState == self.STOP):
            self.directionState = self.LEFT

        elif(cmd == 'right' and self.directionState == self.STOP):
            self.directionState = self.RIGHT

        elif(cmd == 'up_stop' and self.moveState == self.FORWARD):
            self.moveState = self.RELEASE

        elif(cmd == 'down_stop' and self.moveState == self.BACKWARD):
            self.moveState = self.RELEASE

        elif(cmd == 'left_stop' and self.directionState == self.LEFT):
            self.directionState = self.STOP

        elif(cmd == 'right_stop' and self.directionState == self.RIGHT):
            self.directionState = self.STOP
    

    # move forward
    def forward(self):
        if(self.speed >= 100):
            return

        self.speed += 1
        dcMotor.setSpeed(self.speed)
        dcMotor.run(Raspi_MotorHAT.FORWARD)
    
    # move backward
    def backward(self):
        if(self.speed >= 100):
            return

        self.speed += 1
        dcMotor.setSpeed(self.speed)
        dcMotor.run(Raspi_MotorHAT.BACKWARD)

    # turn left
    def left(self):
        if(self.direction <= 300):
            return

        self.direction -= 1
        servo.setPWM(0, 0, self.direction)
        
    # turn right
    def right(self):
        if(self.direction >= 600):
            return

        self.direction += 1
        servo.setPWM(0, 0, self.direction)

    # stop moving
    def moveStop(self):
        self.speed = 0
        dcMotor.setSpeed(self.speed)

    # quit running 
    def exit(self):
        dcMotor.setSpeed(0)
        dcMotor.run(Raspi_MotorHAT.RELEASE)
        servo.setPWM(0, 0, 450)
