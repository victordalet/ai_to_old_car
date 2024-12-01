import cv2
import datetime


def main():
    cap = cv2.VideoCapture(0)

    now = datetime.datetime.now()
    out = cv2.VideoWriter(
        f"output_{now}.mp4", cv2.VideoWriter_fourcc(*"MP4V"), 30, (640, 480)
    )

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            out.write(frame)

            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
