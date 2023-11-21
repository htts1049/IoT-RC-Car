import socketio

sio = socketio.Client()

url = 'http://xxx.xxx.xxx.xxx:3000'

@sio.on('connect')
def on_connect():
    print('connection established')

@sio.on('backend_device')
def on_backend_device(command):
    print('command received with ', command)

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

def device_backend(data):
    sio.emit('device backend', {data: data})

sio.connect(url)

try:
    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()