from src.road_detection.road_detector import RoadDetector
from src.object_detection.tracking import Tracking
from src.object_detection.distance_estimation import DistanceEstimation
import cv2
import sys
from collections import defaultdict
import numpy as np


def main():
    cap = cv2.VideoCapture(sys.argv[1])
    tracking = Tracking("yolov10s.pt")

    video_writer = cv2.VideoWriter(
        "output.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        30,
        (int(cap.get(3)), int(cap.get(4))),
    )

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            lines = RoadDetector.get_lines(frame)
            line_image = RoadDetector.display_lines(frame, lines)
            frame = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
            results_json = tracking.get_detection(frame)

            for res in results_json:
                x1 = int(res["box"]["x1"])
                y1 = int(res["box"]["y1"])
                x2 = int(res["box"]["x2"])
                y2 = int(res["box"]["y2"])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                area_to_object = DistanceEstimation.area_to_object(res)
                cv2.putText(
                    frame,
                    f"Area: {area_to_object}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36, 255, 12),
                    2,
                )

            video_writer.write(frame)

        else:
            break

    video_writer.release()
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
