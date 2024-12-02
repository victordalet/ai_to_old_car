from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    raw_capture = PiRGBArray(camera, size=(640, 480))

    time.sleep(0.1)

    cv2.namedWindow("Frame")

    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    output_file = f"output_{time.time()}.mp4"
    frame_rate = 15.0
    frame_size = (640, 480)

    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, frame_size)

    for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True
    ):
        image = frame.array
        key = cv2.waitKey(1) & 0xFF
        raw_capture.truncate(0)
        video_writer.write(image)
        if key != ord("q"):
            pass
        else:
            video_writer.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
