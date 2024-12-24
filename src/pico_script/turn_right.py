from servo import Servo
import time

serv = Servo(16)

serv.turn_right()

time.sleep(0.2)

serv.destroy()
