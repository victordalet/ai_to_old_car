import cv2
import numpy as np


class RoadDetector:
    def __init__(self):
        pass

    @staticmethod
    def canny(frame: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny

    @staticmethod
    def region_of_interest(frame: np.ndarray) -> np.ndarray:
        height = frame.shape[0]
        polygons = np.array([[(200, height), (1100, height), (550, 250)]])
        mask = np.zeros_like(frame)
        cv2.fillPoly(mask, polygons, 255)
        masked_image = cv2.bitwise_and(frame, mask)
        return masked_image

    @staticmethod
    def display_lines(frame: np.ndarray, lines: np.ndarray) -> np.ndarray:
        line_image = np.zeros_like(frame)
        if lines is not None:
            determine_ligne_deviation = RoadDetector.determine_ligne_deviation(lines)
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image

    @staticmethod
    def get_lines(frame: np.ndarray) -> np.ndarray:
        canny_image = RoadDetector.canny(frame)
        cropped_image = RoadDetector.region_of_interest(canny_image)
        lines = cv2.HoughLinesP(
            cropped_image,
            2,
            np.pi / 180,
            100,
            np.array([]),
            minLineLength=40,
            maxLineGap=5,
        )
        return lines

    @staticmethod
    def determine_ligne_deviation(lines: np.ndarray) -> str:
        left_lines = []
        right_lines = []
        middle_lines = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            slope = (y2 - y1) / (x2 - x1)
            if slope < -0.5:
                right_lines.append(line)
            elif slope > 0.5:
                left_lines.append(line)
            else:
                middle_lines.append(line)
        if len(left_lines) > len(right_lines) and len(left_lines) > len(middle_lines):
            return "left"
        elif len(right_lines) > len(left_lines) and len(right_lines) > len(
            middle_lines
        ):
            return "right"
        else:
            return "middle"
