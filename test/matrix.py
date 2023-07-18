from machine import UART,Pin
import time
uart=UART(1,9600,rx=6,tx=3)
keymap={0:'1',6:'2',12:'3',
        1:'4',7:'5',13:'6',
        2:'7',8:'8',14:'9',
        3:'*',9:'0',15:'#'}

time.sleep(0.5)
while 1:
    re=uart.read()
    if re!=None:
        for k in re:
            print(keymap[k])
    time.sleep_ms(1)
    