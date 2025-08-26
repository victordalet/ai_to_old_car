import os

import torch
import numpy as np
import cv2

from src.const import ACTION_DECISION


class MidasDistanceEstimator:
    def __init__(self, model_type: str):
        self.model_type = model_type
        self.transform = None
        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)

        self.device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.device = (
            self.device
            if os.getenv("USE_CPU", "False").lower()
            not in (
                "true",
                "1",
            )
            else torch.device("cpu")
        )
        self.midas.to(self.device)

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        input_batch = self.transform(frame).to(self.device)

        with torch.no_grad():
            prediction = self.midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=frame.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()

        depth_map = cv2.normalize(
            depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F
        )

        depth_map = (depth_map * 255).astype(np.uint8)
        return depth_map

    def run(self, frame: np.ndarray, threshold, debug) -> str:
        depth_map = self.preprocess(frame)
        median_depth_estimation = int(np.median(depth_map))
        if debug:
            cv2.putText(
                frame,
                f"Median depth: {median_depth_estimation}",
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )
        return (
            ACTION_DECISION[2]
            if median_depth_estimation > threshold
            else ACTION_DECISION[1]
        )
