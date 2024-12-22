from typing import List
import numpy as np


class DistanceEstimation:
    @staticmethod
    def area_to_object(object_detected: dict) -> float:
        x1 = int(object_detected["box"]["x1"])
        y1 = int(object_detected["box"]["y1"])
        x2 = int(object_detected["box"]["x2"])
        y2 = int(object_detected["box"]["y2"])
        area = (x2 - x1) * (y2 - y1)
        return area

    @staticmethod
    def object_is_in_zone(
        object_detected: dict, frame: np.ndarray, left: float, right: float
    ) -> bool:
        x1 = int(object_detected["box"]["x1"])
        x2 = int(object_detected["box"]["x2"])
        object_center = (x1 + x2) / 2
        object_center = object_center / frame.shape[1]
        return left < object_center < right
