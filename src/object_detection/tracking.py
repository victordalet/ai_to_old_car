from ultralytics import YOLO
from typing import Tuple, List
import numpy as np
import json


class Tracking:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def get_detection(self, frame: np.ndarray) -> List:
        results = self.model.track(frame, persist=True)
        results_json = json.loads(results[0].to_json())
        return results_json
