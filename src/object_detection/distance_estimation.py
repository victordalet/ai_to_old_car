from typing import List


class DistanceEstimation:
    @staticmethod
    def area_to_object(object_detected: dict) -> float:
        x1 = int(object_detected["box"]["x1"])
        y1 = int(object_detected["box"]["y1"])
        x2 = int(object_detected["box"]["x2"])
        y2 = int(object_detected["box"]["y2"])
        area = (x2 - x1) * (y2 - y1)
        return area
