import os
import time


class PicoController:
    @staticmethod
    def execute_left_turn():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/turn_left.py")

    @staticmethod
    def execute_right_turn():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/turn_right.py")

    @staticmethod
    def install_micropython():
        os.system("cp ./RPI_PICO-20241129-v1.24.1.uf2 /media/victor/RPI-RP2/")
        time.sleep(10)
        os.system("ampy --port /dev/ttyACM0 put src/pico_script/servo.py")
        time.sleep(2)
        os.system("ampy --port /dev/ttyACM0 put src/pico_script/const.py")
        time.sleep(2)
