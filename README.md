# IoT-RC-Car

운전자 보조 시스템을 탑재한 원격 조종 RC카

| 팀장 | 현상균 ( 라즈베리파이 ) |
| --- | --- |
| 팀원 | 김민형 ( 웹 ) |
| 기간 | 2023.11.20 ~ 2023.11.24 |

---

## UI

![image](https://github.com/htts1049/IoT-RC-Car/assets/130421694/129e336a-ab05-41bf-9215-08914d0c3678)

- RC카 조작은 웹 페이지에서 키보드 입력( wasd / 방향키 ), 마우스 클릭으로 가능합니다.
- 위아래 방향은 전진 및 후진, 좌우측 방향은 좌회전 및 우회전을 의미합니다.
- 조작 입력 시 우측과 같이 화살표가 표시됩니다.
- 흰 색일 경우 해당 방향으로 주행이 가능하고, 검은색일 경우 해당 방향으로 주행이 불가능하며 RC카가 움직이지 않습니다.

![image](https://github.com/htts1049/IoT-RC-Car/assets/130421694/9835e2d9-e936-4ea2-b494-f1ace8837993)

- 좌측은 주행하지 않을 때의 화면입니다.
- 우측은 주행 중 화면으로, 현재 시간과 속도 및 전방 상황을 파악할 수 있습니다.

---

## RC카 제어

https://github.com/htts1049/IoT-RC-Car/assets/130421694/63d04541-5e77-4df5-9d1c-58d463011758

https://github.com/htts1049/IoT-RC-Car/assets/130421694/da3ddaf6-48fe-446e-ac9a-695196c1ce2b



- RC카가 주행하다가 장애물을 만나면 정지합니다.

---

## 라즈베리파이 설정

### 업데이트

```bash
sudo apt-get update
sudo apt-get upgrade
sudo pip3 install --upgrade pip
```

- 패키지 설치에 필요한 apt, pip을 업데이트합니다.

### socketio 설치

```bash
pip install python-socketio
```

- 디바이스와 서버를 연결하는데 필요한 소켓 통신을 설치합니다.
- 하나의 RC카를 제어하기 때문에 MQTT 대신 소켓 통신을 사용했습니다.

### gpiozero 설치

```bash
sudo apt install python3-gpiozero
```

- 초음파 센서 제어에 필요한 gpiozero 패키지를 설치합니다.

```bash
sudo chown root:$USER /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
```

- 저희는 우분투 환경에서 작업하였고, 아래와 같은 에러가 발생했다면 /dev/gpiomem 파일의 권한을 설정해야 합니다.
    
![image](https://github.com/htts1049/IoT-RC-Car/assets/130421694/54c5e9f8-8fb2-4b0d-aa99-42b6c4b55e6c)


### OpenCV 설치

```bash
sudo raspi-config
```

![image](https://github.com/htts1049/IoT-RC-Car/assets/130421694/3fe4d099-63dc-445c-bc3a-397026bb05ac)


- 카메라 설정을 통해 카메라를 활성화해야 합니다.

```bash
sudo apt-get install python3-opencv
```

- 스트리밍 기능을 위해 OpenCV 패키지를 설치합니다.