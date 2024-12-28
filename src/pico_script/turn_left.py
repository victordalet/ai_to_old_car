from servo import Servo
from const import TOP_ARM_MOTOR_PIN
import time

serv = Servo(TOP_ARM_MOTOR_PIN)

serv.turn(180)

time.sleep(1)

serv.destroy()
