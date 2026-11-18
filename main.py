import cv2
import mediapipe as mp
import time
import pyautogui
import math

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Cursor smoothing
smoothening = 5

# Previous cursor position
prev_x, prev_y = 0, 0

# Initialize MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Configure hand detection
options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

# Connections between hand landmarks
connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access webcam!")
    exit()

print("Starting Hand Gesture Detection...")
print("Press Q to exit.")

# Track pinch state
was_pinching = False

# Pinch detection threshold
pinch_threshold = 40

# Create detector
with HandLandmarker.create_from_options(options) as detector:

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read webcam frame.")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Process video frame
        timestamp = time.monotonic_ns() // 1_000_000

        results = detector.detect_for_video(
            mp_image, timestamp
        )

        # Check for detected hands
        if results.hand_landmarks:

            for hand in results.hand_landmarks:

                points = []

                # Convert landmarks into screen coordinates
                for landmark in hand:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    points.append((x, y))

                # Draw connections
                for start, end in connections:
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 255, 255),
                        2
                    )

                # Draw all 21 landmarks
                for x, y in points:
                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Highlight index fingertip (landmark 8)
                # Get index fingertip coordinates
                index_x, index_y = points[8]

                # Map camera coordinates to screen coordinates
                target_x = int(
                    index_x / width * screen_width
                )

                target_y = int(
                    index_y / height * screen_height
                )

                # Smooth cursor movement
                curr_x = prev_x + (target_x - prev_x) // smoothening
                curr_y = prev_y + (target_y - prev_y) // smoothening

                # Move mouse cursor
                pyautogui.moveTo(curr_x, curr_y)

                # Update previous position
                prev_x, prev_y = curr_x, curr_y

                # Get thumb tip coordinates
                thumb_x, thumb_y = points[4]

                # Calculate distance between thumb and index finger
                distance = math.hypot(
                    index_x - thumb_x,
                    index_y - thumb_y
                )

                # Detect pinch gesture
                is_pinching = distance < pinch_threshold

                # Perform one click when pinch starts
                if is_pinching and not was_pinching:
                    pyautogui.click()
                    print("Left Click!")

                # Update pinch state
                was_pinching = is_pinching

                # Display gesture status
                if is_pinching:
                    cv2.putText(
                     frame,
                     "LEFT CLICK",
                     (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    12,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    "HAND DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        else:
            cv2.putText(
                frame,
                "NO HAND DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # Display output
        cv2.imshow(
            "Hand Gesture Cursor Controller",
            frame
        )

        # Exit with Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()

print("Hand tracking stopped.")
