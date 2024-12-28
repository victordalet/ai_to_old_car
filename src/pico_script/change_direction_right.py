from servo import Servo
from const import BOTTOM_ARM_MOTOR_PIN
import time

serv = Servo(BOTTOM_ARM_MOTOR_PIN)

serv.turn(0)

time.sleep(1)

serv.destroy()
