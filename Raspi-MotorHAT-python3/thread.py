import time
import threading

def sub_task(seconds):
    val_sub = 0
    while True:
        print(f' subthread count:{val_sub}\n')
        val_sub += 1
        time.sleep(seconds)


val_main = 0

t = threading.Thread(target=sub_task, args=(2))
t.start()

while True:
    print(f'mainThread count:{val_main}\n')
    val_main += 1
    time.sleep(5)
