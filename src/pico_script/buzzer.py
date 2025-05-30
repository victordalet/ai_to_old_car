from machine import Pin, PWM
import time

PIN_BUZZER = 5
TIME_TO_ACTIVE = 0.5

buzzer = PWM(Pin(PIN_BUZZER), Pin.OUT)

buzzer.active(1)

time.sleep(TIME_TO_ACTIVE)

buzzer.active(0)
