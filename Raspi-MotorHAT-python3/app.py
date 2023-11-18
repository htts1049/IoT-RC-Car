from RC_CAR import *
from DISTANT import getDistance
import threading
import socketio


# Connect server
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server.")

@sio.event
def disconnect():
    print("Disconnected from server.")

sio.connect("http://192.168.26.43:3000")



# Send data to server
def sendData():

    while True:
        distance = getDistance()
        json_data = {'deviceData' : distance}
        sio.emit('deviceData', json_data)


t1 = threading.Thread(target=sendData)
t1.start()



# Drive RC Car
def driveCar():
    while True:
    
        command = input('command : ')
        if command == 'go':
            print("GO")
            go()

        elif command == 'back':
            print("BACK")
            back()

        elif command == 'left':
            print("LEFT")
            left()

        elif command == 'right':
            print("RIGHT")
            right()

        elif command == 'stop':
            print("STOP")
            stop()
        
        elif command == 'mid':
            print("MIDDLE")
            middle()
        
        elif command == 'exit':
            exit()
            t1.join()
            break

t2 = threading.Thread(target=driveCar)
t2.start()

# Exit
t2.join()
sio.wait()
