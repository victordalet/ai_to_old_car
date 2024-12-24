from machine import PWM, Pin


class Servo:
    def __init__(self, number):
        self.servo = PWM(Pin(number))
        self.servo.freq(50)

        self.max_duty = 65025
        self.dig_0 = 0.0725  # 0°
        self.dig_90 = 0.12  # 90°

    def turn_right(self):
        self.servo.duty_u16(int(self.max_duty * self.dig_0))
        self.servo.duty_u16(int(self.max_duty * -self.dig_90))

    def turn_left(self):
        self.servo.duty_u16(int(self.max_duty * self.dig_0))
        self.servo.duty_u16(int(self.max_duty * self.dig_90))

    def destroy(self):
        self.servo.deinit()
