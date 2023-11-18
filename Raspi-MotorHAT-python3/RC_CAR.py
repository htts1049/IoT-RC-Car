from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM

# DC 모터 설정
mh = Raspi_MotorHAT(addr = 0x6F)
myMotor = mh.getMotor(2) # 핀번호
myMotor.setSpeed(100) # 속도

# 서보 모터 설정
servo = PWM(0x6F)
servo.setPWMFreq(60)

def go():
    myMotor.setSpeed(100)
    myMotor.run(Raspi_MotorHAT.FORWARD)

def back():
    myMotor.setSpeed(100)
    myMotor.run(Raspi_MotorHAT.BACKWARD)

def left():
    servo.setPWM(0, 0, 300) #channel num, on, off

def right():
    servo.setPWM(0, 0, 600)

def stop():
    myMotor.run(Raspi_MotorHAT.RELEASE)

def middle():
    servo.setPWM(0, 0, 500)

def exit():
    middle()
    stop() 
