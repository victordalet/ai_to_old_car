from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)
led.toggle()
sleep(5)
led.toggle()
