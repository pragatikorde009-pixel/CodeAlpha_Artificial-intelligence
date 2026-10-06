"""
Task 4: Object Detection and Tracking
CodeAlpha AI Internship

- Real-time video input via OpenCV (webcam or video file)
- Pre-trained YOLOv8 model for object detection
- Built-in ByteTrack algorithm for object tracking (assigns consistent IDs)
- Displays output with labels and tracking IDs in real time
"""

import cv2
from ultralytics import YOLO

# -----------------------------
# CONFIGURATION
# -----------------------------
# Set to 0 for webcam, or replace with a path to a video file, e.g. "sample_video.mp4"
VIDEO_SOURCE = 0

# Model options: yolov8n.pt (fastest), yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt (most accurate)
MODEL_PATH = "yolov8n.pt"

# Tracker config: "bytetrack.yaml" or "botsort.yaml" (both ship with ultralytics)
TRACKER_CONFIG = "bytetrack.yaml"


def main():
    # Load the pre-trained YOLOv8 model (auto-downloads weights on first run)
    model = YOLO(MODEL_PATH)

    # Open video capture (webcam or file)
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print(f"Error: could not open video source {VIDEO_SOURCE}")
        return

    print("Starting object detection and tracking. Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or cannot read frame.")
            break

        # Run detection + tracking on this frame
        # persist=True keeps track of object identities across frames
        results = model.track(frame, persist=True, tracker=TRACKER_CONFIG, verbose=False)

        # results[0].plot() draws bounding boxes, class labels, and tracking IDs
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("Object Detection & Tracking - Task 4", annotated_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
