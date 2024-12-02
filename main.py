from src.road_detection.road_detector import RoadDetector
import cv2


def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            lines = RoadDetector.get_lines(frame)
            line_image = RoadDetector.display_lines(frame, lines)
            combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

            cv2.imshow("frame", combo_image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
