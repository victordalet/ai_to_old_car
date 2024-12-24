from servo import Servo
import time

serv = Servo(16)

serv.turn_left()

time.sleep(0.2)

serv.destroy()
