import picamera
import time


def main():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_recording(f"output_{time.time()}.h264")
    camera.wait_recording(60)
    camera.stop_recording()


if __name__ == "__main__":
    while True:
        main()
