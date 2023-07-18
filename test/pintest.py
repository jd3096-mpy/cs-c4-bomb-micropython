from machine import Pin
import time
tt=Pin(3,Pin.IN,Pin.PULL_UP)

while 1:
    print(tt.value())
    time.sleep(0.1)