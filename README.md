# Hand Gesture Cursor Controller

A real-time virtual mouse controller built using Python, OpenCV, MediaPipe, and PyAutoGUI. This project allows users to control their computer cursor and perform mouse clicks using simple hand gestures captured through a webcam.

## Features

- Real-time hand detection and tracking.
- Tracks 21 hand landmarks using MediaPipe.
- Move the mouse cursor using your index finger.
- Left-click using a thumb and index finger pinch.
- Right-click using a thumb and middle finger pinch.
- Live webcam visualization of detected hand landmarks.

## Technologies Used

- Python
- OpenCV
- MediaPipe Tasks API
- PyAutoGUI
- NumPy

## Project Structure

```text
Hand-Gesture-Cursor-Controller/
├── main.py
├── requirements.txt
├── hand_landmarker.task
└── README.md
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Vignesh-3009/Hand-Gesture-Cursor-Controller.git
```

2. Navigate into the project directory:

```bash
cd Hand-Gesture-Cursor-Controller
```

3. Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

Make sure the `hand_landmarker.task` model file is present in the project directory.

## Usage

1. Start the application.
2. Allow webcam access.
3. Move your index finger to control the cursor.
4. Pinch your thumb and index finger together to left-click.
5. Pinch your thumb and middle finger together to right-click.
6. Press `Q` to exit.

## Hand Landmark Detection

The project uses Google's MediaPipe Hand Landmarker model to detect 21 hand landmarks in real time. Finger coordinates are mapped to screen coordinates to enable cursor movement, while fingertip distances are used to recognize click gestures.

## Future Improvements

- Improved cursor smoothing.
- Adjustable gesture sensitivity.
- Scroll control using hand gestures.
- A graphical user interface.

## Author

**Vignesh Kamath**

GitHub: [Vignesh-3009](https://github.com/Vignesh-3009)
