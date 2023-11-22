import os
from RC_CAR import *
from DISTANCE import *
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
async def sendData():
 
    while True:

        # distance
        up = round(await forwardDistance(), 0)
        left = round(await leftDistance(), 0)
        right = round(await rightDistance(), 0)
        down = round(await backwardDistance(), 0)

        # time
        date = os.popen("date -I").read()
        date = date[0:-1]
        time = os.popen("date +%T").read()
        time = time[0:-1]
        dateTime = date + ' ' + time

        # image
        os.system('fswebcam image.jpg')
        imageFile = open('image.jpg', 'rb')
        imageBlob = imageFile.read()

        # wrap datas in json
        json_data = {
                'dist' :{
                    'up': up,
                    'down': down,
                    'left': left,
                    'right': right,

                    },
                'imageBlob' : imageBlob,
                'dateTime' : dateTime,
                }

        sio.emit('device backend', json_data)

asyncio.run(sendData())

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

t1 = threading.Thread(target=driveCar)
t1.start()

# Exit
t1.join()
rcCar.exit()
sio.wait()