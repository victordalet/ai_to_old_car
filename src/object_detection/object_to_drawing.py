from typing import Dict, List
from src.object_detection.typing_object_detection import JsonDetection
import numpy as np
import cv2


class ObjectToDrawing:
    @staticmethod
    def get_path_picture() -> Dict[str, str]:
        return {
            "car": "assets/car.png",
            "person": "assets/person.png",
            "steering_wheel": "assets/steering_wheel.png",
        }

    @staticmethod
    def load_picture(name: str, frame: np.ndarray, dim: float = 0.05) -> np.ndarray:
        path = ObjectToDrawing.get_path_picture().get(name)
        if path is None:
            raise ValueError(f"Image path for {name} not found.")
        overlay = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        overlay = cv2.resize(
            overlay, (int(frame.shape[1] * dim), int(frame.shape[1] * dim))
        )
        if overlay is None:
            raise ValueError(f"Failed to load image from {path}.")
        return overlay

    @staticmethod
    def return_drawing_debug(
        data: List[JsonDetection],
        frame: np.ndarray,
        overlay_picture: Dict[str, np.ndarray],
        threshold: float = 0.4,
        filter_obj: List[str] = None,
    ) -> np.ndarray:
        if filter_obj is None:
            filter_obj = []
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        cv2.rectangle(
            frame,
            (0, 0),
            (int(frame_width * 0.2), int(frame_height * 0.2)),
            (128, 128, 128),
            -1,
        )
        for res in data:
            if "box" not in res:
                continue
            if res["name"] not in ObjectToDrawing.get_path_picture().keys():
                continue
            if res["confidence"] < threshold or res["name"] in filter_obj:
                continue
            x1 = int(res["box"]["x1"])
            y1 = int(res["box"]["y1"])
            overlay = overlay_picture.get(res["name"])
            overlay_x = x1 * 0.2 - overlay.shape[1] / 2
            overlay_y = y1 * 0.2 - overlay.shape[0] / 2

            for i in range(overlay.shape[0]):
                for j in range(overlay.shape[1]):
                    if overlay[i, j][3] != 0:
                        frame[int(overlay_y) + i, int(overlay_x) + j] = overlay[i, j][
                            :3
                        ]

        return frame

    @staticmethod
    def draw_steering_wheel(
        frame: np.ndarray, picture: np.ndarray, angle: float
    ) -> np.ndarray:
        frame_height, frame_width = frame.shape[:2]
        picture_height, picture_width = picture.shape[:2]

        center = (picture_width // 2, picture_height // 2)

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        rotated_picture = cv2.warpAffine(
            picture,
            rotation_matrix,
            (picture_width, picture_height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT,
        )

        x_offset = frame_width - picture_width
        y_offset = frame_height - picture_height

        for i in range(picture_height):
            for j in range(picture_width):
                if rotated_picture[i, j][3] != 0:
                    frame[y_offset + i, x_offset + j] = rotated_picture[i, j][:3]

        return frame
