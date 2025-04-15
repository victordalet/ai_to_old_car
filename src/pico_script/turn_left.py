from machine import Pin, PWM
from L298N import L298N
import const

ENA1 = PWM(Pin(const.PIN_MOTOR_1))
IN1 = Pin(const.PIN_MOTOR_2, Pin.OUT)
IN2 = Pin(const.PIN_MOTOR_3, Pin.OUT)

ENA2 = PWM(Pin(const.PIN_MOTOR_1))
IN3 = Pin(const.PIN_MOTOR_4, Pin.OUT)
IN4 = Pin(const.PIN_MOTOR_4, Pin.OUT)

motor1 = L298N(ENA1, IN1, IN2)

motor1.setSpeed(25000)

motor1.forward()
time.sleep(const.TIME_TO_RUN)
motor1.stop()
