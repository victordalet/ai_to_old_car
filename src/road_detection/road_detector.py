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
            determine_ligne_deviation = RoadDetector.determine_ligne_deviation(lines, frame)
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            cv2.line(
                line_image,
                (int(frame.shape[1] / 2), frame.shape[0]),
                (int(frame.shape[1] / 2), 0),
                (0, 0, 255),
                10,
            )
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
    def determine_ligne_deviation(lines: np.ndarray, frame: np.ndarray) -> str:
        left = 0
        right = 0
        for line in lines:
            if line[0][0] < frame.shape[1] / 2:
                if line[0][2] > frame.shape[1] / 2:
                    left += 1
            else:
                if line[0][2] < frame.shape[1] / 2:
                    right += 1
        print("left: ", left)
        print("right: ", right)
        if left > right:
            return "left"
        return "right"
