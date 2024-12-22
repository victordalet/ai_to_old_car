from src.road_detection.road_detector import RoadDetector
from src.object_detection.tracking import Tracking
from src.object_detection.distance_estimation import DistanceEstimation
import cv2
import sys
from collections import defaultdict
import numpy as np
from typing import List

MAX_AREA = 8000
MAX_ARRAY_DECISION_SIZE = 20
LEFT_CENTER = 0.3
RIGHT_CENTER = 0.8


class Main:
    def __init__(self):
        self.cap = cv2.VideoCapture(sys.argv[1])
        self.tracking = Tracking("yolov10s.pt")
        self.road_decision: List[str] = []
        self.detection_decision: List[str] = []

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

    def pipeline(self):
        video_writer = cv2.VideoWriter(
            "output.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (int(self.cap.get(3)), int(self.cap.get(4))),
        )

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                lines = RoadDetector.get_lines(frame)
                line_image = RoadDetector.display_lines(frame, lines)
                deviation_position = RoadDetector.determine_ligne_deviation(lines)
                self.road_decision.append(deviation_position)
                frame = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
                results_json = self.tracking.get_detection(frame)

                for res in results_json:
                    x1 = int(res["box"]["x1"])
                    y1 = int(res["box"]["y1"])
                    x2 = int(res["box"]["x2"])
                    y2 = int(res["box"]["y2"])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    area_to_object = DistanceEstimation.area_to_object(res)
                    if DistanceEstimation.object_is_in_zone(
                        res, frame, LEFT_CENTER, RIGHT_CENTER
                    ):
                        if area_to_object > MAX_AREA:
                            self.detection_decision.append(
                                "left" if x1 > frame.shape[1] / 2 else "right"
                            )
                        else:
                            if len(self.detection_decision) != 0:
                                self.detection_decision.pop(0)
                    cv2.putText(
                        frame,
                        f"Area: {area_to_object}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (36, 255, 12),
                        2,
                    )

                action = self.get_decision()
                cv2.line(
                    frame,
                    (int(frame.shape[1] * LEFT_CENTER), 0),
                    (int(frame.shape[1] * LEFT_CENTER), frame.shape[0]),
                    (0, 0, 255),
                    1,
                )
                cv2.line(
                    frame,
                    (int(frame.shape[1] * RIGHT_CENTER), 0),
                    (int(frame.shape[1] * RIGHT_CENTER), frame.shape[0]),
                    (0, 0, 255),
                    1,
                )
                cv2.putText(
                    frame,
                    f"Action: {action}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (36, 255, 12),
                    2,
                )

                video_writer.write(frame)

            else:
                break

        video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    Main().pipeline()
