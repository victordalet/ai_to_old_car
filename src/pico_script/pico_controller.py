import os
import time


class PicoController:
    @staticmethod
    def execute_left_turn():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/left_turn.py")

    @staticmethod
    def execute_right_turn():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/right_turn.py")

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
    def execute_test_connection():
        os.system("ampy --port /dev/ttyACM0 run src/pico_script/test_connection.py")

    @staticmethod
    def install_micropython():
        os.system("cp ./RPI_PICO-20241129-v1.24.1.uf2 /media/victor/RPI-RP2")
        time.sleep(10)
