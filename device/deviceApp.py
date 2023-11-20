import os
from RC_CAR import *
from DISTANT import getDistance
import threading
import socketio
import time

rcCar = rcCar()

# Connect server
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server.")

@sio.on('backend device')
def backend_device(cmd):
    rcCar.setState(cmd)

@sio.event
def disconnect():
    print("Disconnected from server.")

sio.connect("http://192.168.26.43:3000")



# Send data to server
def sendData():
    while True:

        # distance
        distance = getDistance()
        
        # image
        # os.system('fswebcam ./image.jpg')
        # image_file = open('./image.jpg', 'rb')
        # image_blob = image_file.read()

        # wrap datas in json
        json_data = {
                'distance' : distance,
                # 'imageBlob' : image_blob
                }


        sio.emit('deviceData', json_data)
        time.sleep(0.1)


t1 = threading.Thread(target=sendData)
t1.start()



# Drive RC car according to state
def driveCar():
    while True:
        if(rcCar.moveState == rcCar.FORWARD):
            rcCar.forward()

        elif(rcCar.moveState == rcCar.RELEASE):
            rcCar.moveStop()

        elif(rcCar.moveState == rcCar.BACKWARD):
            rcCar.backward()

        if(rcCar.directionState == rcCar.LEFT):
            rcCar.left()

        elif(rcCar.directionState == rcCar.RIGHT):
            rcCar.right()


t2 = threading.Thread(target=driveCar)
t2.start()
  

# Exit
t1.join()
t2.join()
rcCar.exit()
sio.wait()
