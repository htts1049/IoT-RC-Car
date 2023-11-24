import os
import threading
import socketio
import cv2
from time import sleep
from RC_CAR import *
from DISTANCE import *


# Configure
rcCar = rcCar()
rcCar.quit()
cap = cv2.VideoCapture(0, cv2.CAP_V4L)


# Connect server
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server.")

@sio.on('backend device')
def backend_device(cmd):
    print(cmd == "up_press")
    rcCar.setState(cmd)

@sio.event
def disconnect():
    print("Disconnected from server.")


# Drive RC car according to state
def driveCar(car):
    if(car.moveState == car.FORWARD):
        car.forward()

    elif(car.moveState == car.RELEASE):
        car.moveStop()

    elif(car.moveState == car.BACKWARD):
        car.backward()

    if(car.directionState == car.LEFT):
        car.left()

    elif(car.directionState == car.RIGHT):
        car.right()

    if(car.moveState == car.STOP and car.directionState == car.STOP):
        car.quit()
    
    return car.moveState, car.directionState


# Send data to server
async def sendData(car):

    while True:
        
        # get distance
        up = round(await forwardDistance(), 6)
        down = round(await backwardDistance(), 6)

        # get time
        date = os.popen("date -I").read()
        date = date[0:-1]
        time = os.popen("date +%T").read()
        time = time[0:-1]
        nanosecond = os.popen("date +%N").read()
        nanosecond = nanosecond[0:-1]
        dateTime = date + ' ' + time + '.' + nanosecond

        # get image
        _, img = cap.read()
        img = cv2.flip(img, -1)
        _, imageEncoded = cv2.imencode('.jpg', img)
        imageBlob = imageEncoded.tobytes()

        # wrap datas in json
        json_data = {
                'dist' :{
                    'up': up,
                    'down': down,
                    },
                'imageBlob' : imageBlob,
                'dateTime' : dateTime,
                'speed' : car.speed,
                'off' : False,
                }

        # drive RC car
        if(driveCar(car) == (car.OFF, car.OFF)):
            car.quit()
            json_data['off'] = True
            sio.emit('device backend', json_data)
            sleep(2)
            sio.disconnect()
            return

        # send datas to server
        sio.emit('device backend', json_data)


def main():
    sio.connect("http://192.168.26.43:3000")
    asyncio.run(sendData(rcCar))
    sio.wait()


if __name__ == "__main__":
    main()