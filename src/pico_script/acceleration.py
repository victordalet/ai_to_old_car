from servo import Servo
from const import ACCELERATOR_MOTOR_PIN
import time

serv = Servo(ACCELERATOR_MOTOR_PIN)

serv.turn(180)

time.sleep(2)

serv.turn(0)

time.sleep(0.5)

serv.destroy()
