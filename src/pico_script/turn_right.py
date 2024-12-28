from servo import Servo
from const import TOP_ARM_MOTOR_PIN
import time

serv = Servo(TOP_ARM_MOTOR_PIN)

serv.turn(0)

time.sleep(1)

serv.destroy()
