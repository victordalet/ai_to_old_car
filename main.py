from src.const import (
    PERCENTAGE_MOVEMENT,
    YOLO_MODEL,
    MIDAS_MODEL,
    CAMERA_SOURCE,
    ACTION_DECISION,
    MAX_SIZE_STACK_ROAD_DECISION,
    MIDAS_DISTANCE_THRESHOLD,
)
from src.midas_distance_estimator import MidasDistanceEstimator
from src.movement_detector import MovementDetector
from src.object_detection.tracking import Tracking
from src.pico_script.pico_controller import PicoController
import cv2
import os
from typing import List

from src.road_decision import RoadDecision

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")


class Main:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_SOURCE)
        self.tracking = Tracking(YOLO_MODEL)
        self.depth_estimator = MidasDistanceEstimator(MIDAS_MODEL)
        self.movement_detector = MovementDetector(PERCENTAGE_MOVEMENT)
        self.road_decision = RoadDecision()
        self.road_decision_stack: List[str] = []

    @staticmethod
    def execute_action(action: str):
        if action == "left":
            PicoController.execute_left_turn()
        elif action == "right":
            PicoController.execute_right_turn()

    def pipeline(self):
        video_writer = None
        if DEBUG:
            video_writer = cv2.VideoWriter(
                "output.mp4",
                cv2.VideoWriter_fourcc(*"mp4v"),
                30,
                (int(self.cap.get(3)), int(self.cap.get(4))),
            )

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                if self.movement_detector.is_in_action_frame(frame, DEBUG):
                    self.road_decision_stack.append(
                        self.depth_estimator.run(frame, MIDAS_DISTANCE_THRESHOLD, DEBUG)
                    )
                else:
                    self.road_decision_stack.append(ACTION_DECISION[0])
                action = self.road_decision.decide(self.road_decision_stack)
                if len(self.road_decision_stack) > MAX_SIZE_STACK_ROAD_DECISION:
                    self.road_decision_stack.pop(0)
                if DEBUG:
                    cv2.putText(
                        frame,
                        f"Action: {action}",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0) if action != ACTION_DECISION[2] else (0, 0, 255),
                        2 if action != ACTION_DECISION[2] else 3,
                    )
                else:
                    self.execute_action(action)

                if DEBUG and video_writer is not None:
                    video_writer.write(frame)

            else:
                break

        if DEBUG and video_writer is not None:
            video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    if not DEBUG:
        PicoController.install_micropython()
    Main().pipeline()
