import cv2
import sys

import numpy as np
import torch


class Main:
    def __init__(self):
        self.cap = cv2.VideoCapture(sys.argv[1])

    def pipeline(self):
        video_writer = cv2.VideoWriter(
            "output.mp4",
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (int(self.cap.get(3)), int(self.cap.get(4))),
        )

        model_type = "MiDaS_small"

        midas = torch.hub.load("intel-isl/MiDaS", model_type)

        device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        midas.to(device)
        midas.eval()

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            transform = midas_transforms.dpt_transform
        else:
            transform = midas_transforms.small_transform

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            input_batch = transform(frame).to(device)

            with torch.no_grad():
                prediction = midas(input_batch)

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
            frame = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)

            video_writer.write(frame)

        video_writer.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test/test_distance_detection.py " "<video_path> ")
        sys.exit(1)
    Main().pipeline()
