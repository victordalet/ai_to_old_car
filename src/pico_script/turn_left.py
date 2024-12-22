import machine
import utime

servo = machine.PWM(machine.Pin(15))  # signal PWM à la broche GP 15
servo.freq(50)

servo.duty_u16(3500)
