from src.road_detection.road_detector import RoadDetector
from src.object_detection.tracking import Tracking
from src.object_detection.distance_estimation import DistanceEstimation
from src.pico_script.pico_controller import PicoController
import cv2
import os
from collections import defaultdict
import numpy as np
from typing import List

MAX_AREA = 40000
MAX_ARRAY_DECISION_SIZE = 20


FILTERED_CLASSES = ["person"]


class Main:
    def __init__(self):
        self.cap = cv2.VideoCapture(4)
        self.tracking = Tracking("yolov10s.pt")
        self.road_decision: List[str] = []
        self.detection_decision: List[str] = []
        self.last_action = "left"
        self.active_road_detection = True
        self.active_object_detection = True

    def get_decision(self) -> str:
        if len(self.detection_decision) > 5:
            return self.detection_decision[-1]
        if len(self.road_decision) < 5:
            return "straight"
        if self.road_decision[-5:] == ["right"] * 5:
            return "right"
        if self.road_decision[-5:] == ["left"] * 5:
            return "left"
        return "straight"

    def execute_action(self, action: str):
        if self.last_action != action:
            if self.last_action == "left":
                PicoController.execute_change_direction_right()
            else:
                PicoController.execute_change_direction_left()
            self.last_action = action
        if action == "left":
            PicoController.execute_left_turn()
        elif action == "right":
            PicoController.execute_right_turn()

    def pipeline(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, -1)

            if ret:
                if self.active_road_detection:
                    lines = RoadDetector.get_lines(frame)
                    line_image = RoadDetector.display_lines(frame, lines)
                    deviation_position = RoadDetector.determine_ligne_deviation(lines)
                    self.road_decision.append(deviation_position)
                    frame = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

                if self.active_object_detection:
                    results_json = self.tracking.get_detection(frame)

                    for res in results_json:
                        if res["name"] not in FILTERED_CLASSES:
                            continue

                        x1 = int(res["box"]["x1"])
                        y1 = int(res["box"]["y1"])
                        x2 = int(res["box"]["x2"])
                        y2 = int(res["box"]["y2"])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        area_to_object = DistanceEstimation.area_to_object(res)
                        if area_to_object > MAX_AREA:
                            self.detection_decision.append(
                                "left" if x1 > frame.shape[1] / 2 else "right"
                            )
                        else:
                            if len(self.detection_decision) > 1:
                                self.detection_decision.pop(0)

                action = self.get_decision()
                self.execute_action(action)
                if os.getenv("DEBUG", False):
                    cv2.imshow("frame", frame)

            else:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    PicoController.install_micropython()
    PicoController.execute_test_connection()
    Main().pipeline()
