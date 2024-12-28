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
    def execute_change_direction_left():
        os.system(
            "ampy --port /dev/ttyACM0 run src/pico_script/change_direction_left.py"
        )

    @staticmethod
    def execute_change_direction_right():
        os.system(
            "ampy --port /dev/ttyACM0 run src/pico_script/change_direction_right.py"
        )

    @staticmethod
    def execute_braking():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/braking.py")

    @staticmethod
    def execute_acceleration():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/acceleration.py")

    @staticmethod
    def execute_test_connection():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/test_connection.py")

    @staticmethod
    def install_micropython():
        os.system("cp ./RPI_PICO-20241129-v1.24.1.uf2 /media/victor/RPI-RP2/")
        time.sleep(10)
        os.system("ampy --port /dev/ttyACM0 put src/pico_script/servo.py")
        time.sleep(2)
        os.system("ampy --port /dev/ttyACM0 put src/pico_script/const.py")
        time.sleep(2)
