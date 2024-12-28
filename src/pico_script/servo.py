from machine import Pin, PWM


class Servo:
    def __init__(self, number, freq=50):
        self.pin = Pin(number, Pin.OUT)
        self.servo = PWM(self.pin)
        self.servo.freq(freq)
        self.duty = 0

    def turn(self, angle):
        self.duty = int(angle / 18 + 2)
        self.servo.duty_u16(self.duty * 65535 // 100)

    def get_actual_duty(self):
        return self.duty

    def destroy(self):
        self.servo.deinit()
        self.pin.deinit()
