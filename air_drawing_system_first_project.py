import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- MODEL ----------------
base_options = python.BaseOptions(
    model_asset_path=r"C:\Users\SANGEETHA\AppData\Local\Programs\Python\Python313\hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

canvas = None

xp, yp = 0, 0
prev_x, prev_y = 0, 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:

        h, w, _ = frame.shape
        hand = result.hand_landmarks[0]

        x = int(hand[8].x * w)
        y = int(hand[8].y * h)

        # Strong smoothing
        if prev_x == 0:
            prev_x = x
            prev_y = y

        x = int(prev_x * 0.9 + x * 0.1)
        y = int(prev_y * 0.9 + y * 0.1)

        prev_x = x
        prev_y = y

        # Finger states
        index_up = hand[8].y < hand[6].y
        middle_up = hand[12].y < hand[10].y
        ring_up = hand[16].y < hand[14].y
        pinky_up = hand[20].y < hand[18].y

        # Draw only when only index finger is up
        draw_mode = (
            index_up and
            not middle_up and
            not ring_up and
            not pinky_up
        )

        cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)

        if draw_mode:

            if xp == 0:
                xp, yp = x, y

            distance = ((x - xp) ** 2 + (y - yp) ** 2) ** 0.5

            # Ignore jitter
            if distance < 5:
                pass

            # Ignore huge jumps
            elif distance > 50:
                xp, yp = x, y

            else:
                cv2.line(
                    canvas,
                    (xp, yp),
                    (x, y),
                    (255, 0, 0),
                    5
                )
                xp, yp = x, y

            cv2.putText(
                frame,
                "DRAW",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        else:
            xp, yp = 0, 0

            cv2.putText(
                frame,
                "MOVE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    else:
        xp, yp = 0, 0
        prev_x, prev_y = 0, 0

    output = cv2.add(frame, canvas)

    cv2.putText(
        output,
        "C = Clear    Q = Quit",
        (10, 470),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("Air Drawing System", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas = np.zeros_like(frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
