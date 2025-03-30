from src.road_detection.road_detector import RoadDetector
from src.object_detection.tracking import Tracking
from src.object_detection.distance_estimation import DistanceEstimation
from src.object_detection.object_to_drawing import ObjectToDrawing
import cv2
import sys
from collections import defaultdict
import numpy as np
from typing import List

MAX_AREA = 2500
MAX_ARRAY_DECISION_SIZE = 20
LEFT_CENTER = 0.3
RIGHT_CENTER = 0.8

FILTERED_CLASSES = ["person"]


class Main:
    def __init__(self):
        self.cap = cv2.VideoCapture(sys.argv[1])
        self.tracking = Tracking("yolov10s.pt")
        self.road_decision: List[int] = []
        self.detection_decision: List[int] = []
        self.active_road_detection: bool = True if sys.argv[2] == "True" else False
        self.active_object_detection: bool = True if sys.argv[3] == "True" else False
        self.active_drawing: bool = True if sys.argv[4] == "True" else False

    def get_decision(self) -> int:
        if len(self.detection_decision) > 5:
            return self.detection_decision[-1]
        if len(self.road_decision) < 1:
            return 0
        return self.road_decision[-1]

    def pipeline(self):
        video_writer = cv2.VideoWriter(
            "output.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (int(self.cap.get(3)), int(self.cap.get(4))),
        )
        steering_wheel = ObjectToDrawing.load_picture(
            "steering_wheel", self.cap.read()[1], 0.2
        )
        picture_dict = {
            "car": ObjectToDrawing.load_picture("car", self.cap.read()[1]),
            "person": ObjectToDrawing.load_picture("person", self.cap.read()[1]),
        }

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                if self.active_road_detection:
                    lines = RoadDetector.get_lines(frame)
                    line_image = RoadDetector.display_lines(frame, lines)
                    deviation_position = RoadDetector.determine_ligne_deviation(lines)
                    self.road_decision.append(deviation_position)
                    frame = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

                if self.active_object_detection:
                    results_json = self.tracking.get_detection(frame)

                    if self.active_drawing:
                        frame = ObjectToDrawing.return_drawing_debug(
                            results_json, frame, picture_dict, filter_obj=["person"]
                        )

                    for res in results_json:
                        if res["name"] not in FILTERED_CLASSES:
                            continue

                        x1 = int(res["box"]["x1"])
                        y1 = int(res["box"]["y1"])
                        x2 = int(res["box"]["x2"])
                        y2 = int(res["box"]["y2"])

                        area_to_object = DistanceEstimation.area_to_object(res)
                        if DistanceEstimation.object_is_in_zone(
                            res, frame, LEFT_CENTER, RIGHT_CENTER
                        ):
                            if area_to_object > MAX_AREA:
                                self.detection_decision.append(
                                    90 if x1 > frame.shape[1] / 2 else -90
                                )
                            else:
                                if len(self.detection_decision) != 0:
                                    self.detection_decision.pop(0)

                deg = self.get_decision()

                if self.active_drawing:
                    ObjectToDrawing.draw_steering_wheel(frame, steering_wheel, deg)

                video_writer.write(frame)

            else:
                break

        video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python test/test_road_detection.py "
            "<video_path> "
            "<active_road_detection> "
            "<active_object_detection> "
            "<active_drawing>"
        )
        sys.exit(1)
    Main().pipeline()
