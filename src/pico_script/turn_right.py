from machine import Pin, PWM
from L298N import L298N
import const

ENA2 = PWM(Pin(const.PIN_MOTOR_1))
IN3 = Pin(const.PIN_MOTOR_4, Pin.OUT)
IN4 = Pin(const.PIN_MOTOR_4, Pin.OUT)

motor2 = L298N(ENA2, IN3, IN4)

motor2.setSpeed(25000)
