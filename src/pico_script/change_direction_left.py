from servo import Servo
import time

serv = Servo(17)

serv.turn_left()

time.sleep(1)

serv.destroy()
