from ultralytics import YOLO
from typing import List
import numpy as np
import json
import cv2

from src.const import RED_RATION_TRAFFIC_LIGHT


class Tracking:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def get_detection(self, frame: np.ndarray) -> List:
        results = self.model(frame, verbose=False)
        results_json = json.loads(results[0].to_json())
        return results_json

    def detect_object(self, frame: np.ndarray, object_to_detect: List[str]) -> bool:
        for result in self.get_detection(frame):
            for obj in result["boxes"]:
                if obj["class"] in object_to_detect:
                    return True
        return False

    def detect_red_traffic_light(self, frame: np.ndarray, debug: bool) -> bool:
        detections = self.get_detection(frame)
        for obj in detections:
            if obj["name"] == "traffic light":
                x1, y1, x2, y2 = (
                    int(obj["box"]["x1"]),
                    int(obj["box"]["y1"]),
                    int(obj["box"]["x2"]),
                    int(obj["box"]["y2"]),
                )
                traffic_light_roi = frame[y1:y2, x1:x2]
                hsv_roi = cv2.cvtColor(traffic_light_roi, cv2.COLOR_BGR2HSV)

                lower_red1 = np.array([0, 100, 100])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([160, 100, 100])
                upper_red2 = np.array([180, 255, 255])

                mask1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
                red_mask = cv2.bitwise_or(mask1, mask2)

                red_pixel_count = cv2.countNonZero(red_mask)
                total_pixel_count = (
                    traffic_light_roi.shape[0] * traffic_light_roi.shape[1]
                )
                red_ratio = red_pixel_count / total_pixel_count

                if debug:
                    color = (
                        (0, 0, 255)
                        if red_ratio > RED_RATION_TRAFFIC_LIGHT
                        else (0, 255, 0)
                    )
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"Red Ratio: {red_ratio:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )

                if red_ratio > RED_RATION_TRAFFIC_LIGHT:
                    return True
        return False
