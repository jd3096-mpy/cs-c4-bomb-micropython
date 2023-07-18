from machine import Pin,UART,SoftI2C,Timer
import time
from lcd1601 import LCD

lcd = LCD(SoftI2C(scl=Pin(3), sda=Pin(12), freq=100000))
lcd.puts("    ********   ")

led=Pin(0,Pin.OUT)
led.off()

buzzer=Pin(1,Pin.OUT)
buzzer.off()

busy=Pin(10,Pin.IN,Pin.PULL_DOWN)

uart=UART(1,9600,tx=7,rx=6)

BOMB_PLANT=const(1)
BOMB_BOOM=const(2)
BOMB_DEF=const(3)
CT_WIN=const(4)
TE_WIN=const(5)

keymap={0:'1',6:'2',12:'3',
        1:'4',7:'5',13:'6',
        2:'7',8:'8',14:'9',
        3:'*',9:'0',15:'#'}

start_time=0
total_time=0

def wait_voice():
    time.sleep(0.5)
    while busy.value():
        print('play')
    print('end')
    time.sleep(0.5)
    
def play_voice(cmd):
    if cmd==1:
        uart.write('A7:00001')
    elif cmd==2:
        uart.write('A7:00002')
    elif cmd==3:
        uart.write('A7:00003')
    elif cmd==4:
        uart.write('A7:00004')
    elif cmd==5:
        uart.write('A7:00005')
        

def blink():
    buzzer.on()
    led.on()
    time.sleep_ms(50)
    buzzer.off()
    led.off()

def beep():
    buzzer.on()
    time.sleep_ms(50)
    buzzer.off()


def show_pwd(pwd):
    seven_bits="*"*(8-len(pwd))+pwd
    print(seven_bits)
    lcd.puts("    "+seven_bits+"   ")
    
def count_down(t):
    global start_time,total_time
    ct=int((total_time*1000+300-time.ticks_ms()+start_time)/10)
    if ct<0:
        lcd.puts('EXPLODE>>> 00:00')
    else:
        ss=str(ct//100)
        st="0"*(2-len(ss))+ss
        mm=str(ct%100)
        t=str(st)+':'+str(mm)
        lcd.puts('EXPLODE>>> '+t)


def bomb_set():
    led.on()
    pwd=''
    plant=False
    while 1:
        if plant:
            break
        re=uart.read()
        #print(re)
        if re!=None:
            print(re)
            for k in re:
                try:
                    if keymap[k]=='*':
                        if pwd!='':
                            pwd=pwd[:-1]
                            show_pwd(pwd)
                    elif keymap[k]=='#':
                        if pwd=='7355608':
                            plant=True
                        else:
                            lcd.puts("  Password Err ")
                            pwd=''
                            time.sleep(1)
                            lcd.puts("    ********   ")
                        beep()
                    else:
                        if len(pwd)<8:
                            pwd+=keymap[k]
                            show_pwd(pwd)
                            beep()
                            
                except:
                    pass
    play_voice(BOMB_PLANT)
    lcd.puts("  Bomb Planted! ")
     
def bomb_countdown(t):
    global start_time,total_time
    total_time=t
    start_time=time.ticks_ms()
    tim=Timer(0)
    tim.init(period=10, callback=count_down)
    interval=1000
    bt=t

    for i in range(0,bt-10):
        blink()
        time.sleep(0.95)

    print('speed up')

    start=time.time()
    while 1:
        if time.time()-start>10:
            break
        blink()
        time.sleep_ms(int(interval))
        interval=interval/1.15
    play_voice(BOMB_BOOM)
    tim.deinit()
    time.sleep(0.5)
    lcd.puts("    Big Boom!   ")
                
bomb_set()
time.sleep(1)
bomb_countdown(14)
wait_voice()
play_voice(TE_WIN)

    





