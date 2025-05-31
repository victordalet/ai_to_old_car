from machine import Pin
import time

PIN_NUMBER = 15
TIMEOUT = 0.5

pin = Pin(PIN_NUMBER, Pin.OUT)

pin.value(1)

time.sleep(TIMEOUT)

pin.value(0)
