from machine import Pin, SoftI2C
from lcd1601 import LCD
scl_pin = 3
sda_pin = 12
lcd = LCD(SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000))
lcd.puts("  >>**13123<<")
