from src.road_detection.road_detector import RoadDetector
from src.object_detection.tracking import Tracking
import cv2
import sys
from collections import defaultdict
import numpy as np


def main():
    cap = cv2.VideoCapture(sys.argv[1])
    tracking = Tracking("yolov10s.onnx")

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            lines = RoadDetector.get_lines(frame)
            line_image = RoadDetector.display_lines(frame, lines)
            frame = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

            results_json = tracking.get_detection(frame)

            for res in results_json:
                x1 = res["box"]["x1"]
                y1 = res["box"]["y1"]
                x2 = res["box"]["x2"]
                y2 = res["box"]["y2"]
                x3 = res["box"]["x3"]
                y3 = res["box"]["y3"]
                x4 = res["box"]["x4"]
                y4 = res["box"]["y4"]
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (0, 255, 0), 2)
                cv2.line(frame, (int(x3), int(y3)), (int(x4), int(y4)), (0, 255, 0), 2)
                cv2.line(frame, (int(x4), int(y4)), (int(x1), int(y1)), (0, 255, 0), 2)

            cv2.imshow("frame", frame)

            # si j'appuie sur la touche e alors je passe à la frame suivante sinon on attend
            if cv2.waitKey(0) & 0xFF == 101:
                continue

        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
