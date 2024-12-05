import time
import picamera2

camera = picamera2.Picamera2()
camera.resolution = (640, 480)
while True:
    print(time.time())
    camera.start_and_record_video(f"output_{time.time()}.mp4", duration=20)
