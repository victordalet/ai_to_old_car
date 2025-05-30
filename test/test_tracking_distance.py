from src.object_detection.tracking import Tracking
from src.object_detection.distance_estimation import DistanceEstimation
from src.object_detection.object_to_drawing import ObjectToDrawing
from src.pico_script.pico_controller import PicoController
import cv2
import sys
from typing import List

MAX_AREA = 2500
MAX_ARRAY_DECISION_SIZE = 20

FILTERED_CLASSES = ["person"]


class Main:
    def __init__(self):
        self.tracking = Tracking("yolov10s.pt")
        self.road_decision: List[int] = []
        self.detection_decision: List[int] = []
        self.only_record = True if sys.argv[2] == "true" else False
        if self.only_record:
            self.cap = cv2.VideoCapture(sys.argv[1])
        else:
            self.cap = cv2.VideoCapture(int(sys.argv[1]))

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
        picture_dict = {
            "car": ObjectToDrawing.load_picture("car", self.cap.read()[1]),
            "person": ObjectToDrawing.load_picture("person", self.cap.read()[1]),
        }

        if not self.only_record:
            PicoController.install_micropython(lite=True)

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                results_json = self.tracking.get_detection(frame)

                for res in results_json:
                    if res["name"] not in FILTERED_CLASSES:
                        continue

                    x1 = int(res["box"]["x1"])
                    y1 = int(res["box"]["y1"])
                    x2 = int(res["box"]["x2"])
                    y2 = int(res["box"]["y2"])

                    area_to_object = DistanceEstimation.area_to_object(res)
                    if area_to_object > MAX_AREA:
                        self.detection_decision.append(
                            90 if x1 > frame.shape[1] / 2 else -90
                        )
                    else:
                        if len(self.detection_decision) != 0:
                            self.detection_decision.pop(0)

                deg = self.get_decision()

                if deg != 0:
                    if self.only_record:
                        cv2.putText(
                            frame,
                            f"Alert",
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2,
                        )
                    else:
                        print("Alert")
                        PicoController.active_buzzer()

                video_writer.write(frame)

            else:
                break

        video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python test/test_tracking_distance.py "
            "<video_path> "
            "<only_record>"
        )
        sys.exit(1)
    Main().pipeline()
