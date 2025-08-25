import cv2


class MovementDetector:
    def __init__(self, percentage_movement=40):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.percentage_movement = percentage_movement

    def is_in_action_frame(self, frame, debug):
        fg_mask = self.background_subtractor.apply(frame)
        non_zero_count = cv2.countNonZero(fg_mask)
        total_pixels = frame.shape[0] * frame.shape[1]
        movement_percentage = (non_zero_count / total_pixels) * 100
        if debug:
            cv2.putText(
                frame,
                f"Movement: {movement_percentage:.2f}%",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (
                    (0, 255, 0)
                    if movement_percentage > self.percentage_movement
                    else (0, 0, 255)
                ),
                2,
            )
        return movement_percentage > self.percentage_movement
