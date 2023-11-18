import socketio
import base64
import json



sio = socketio.Client()

image_file = open("test.jpg", "rb")
image_binary = image_file.read()
encoded_string = base64.b64encode(image_binary)


def send_image(image_path):
    with open(image_path, "rb") as image_file:

        image_binary = image_file.read()
     
        # Encode the image as Base64
        # encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        

        json_data = {'deviceData' : image_binary }

        # Send the encoded image to the server
        sio.emit('deviceData', json_data)


@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

# Connect to the server
sio.connect('http://192.168.26.43:3000')

send_image('./test.jpg')

# Keep the program running
sio.wait()
image_file.close()
