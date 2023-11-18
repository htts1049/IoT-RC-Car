# IoT-RC-Car

IoT RC Car with Driver Assistance System

---

## Outline

not written yet

---

## Configuration

### update

```bash
sudo apt update
sudo pip3 install --upgrade pip
```

- First, update apt and pip3.

### install socketio

```bash
pip install python-socketio
```

- Install socket.io to connect to the server.
- We only control one RC Car, so we didn’t use MQTT which is designed to control multiple devices.

### install gpiozero

```bash
sudo apt install python3-gpiozero
sudo chown root:$USER /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
```

- Install gpiozero to control ultrasonic sensor.
- We had runtime error like this. If it doesn’t occur, you don’t need to change authority of /dev/gpiomem.
    
    ![초음파 트러블 슈팅](https://github.com/htts1049/IoT-RC-Car/assets/130421694/8d517815-0706-4213-a796-21bb2045ee1c)