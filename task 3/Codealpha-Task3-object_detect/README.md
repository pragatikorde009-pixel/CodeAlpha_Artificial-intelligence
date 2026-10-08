# Task 4: Object Detection and Tracking

CodeAlpha AI Internship submission.

## What this does
- Captures real-time video (webcam or a video file) using OpenCV
- Detects objects in each frame using a pre-trained YOLOv8 model
- Tracks detected objects across frames using ByteTrack, assigning each a consistent ID
- Displays the live output with bounding boxes, class labels, and tracking IDs

## Setup

1. Make sure Python 3.8+ is installed:
   ```
   python --version
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

```
python detect_track.py
```

- A window will open showing your webcam feed with detected objects boxed, labeled, and tracked.
- Press `q` to quit.

## Using a video file instead of a webcam

Open `detect_track.py` and change this line near the top:

```python
VIDEO_SOURCE = 0
```

to:

```python
VIDEO_SOURCE = "your_video_file.mp4"
```

Place your video file in this same folder.

## Notes for submission

- **Model used:** YOLOv8n (nano) — pre-trained, fast, good for real-time demos
- **Tracking algorithm:** ByteTrack (built into `ultralytics`, functionally equivalent to SORT/DeepSORT for this task's requirements)
- For your submission, include a short screen recording or a few screenshots of the detection window running with visible bounding boxes and tracking IDs.

## Troubleshooting

- **First run is slow:** YOLOv8 weights (~6MB) download automatically the first time you run the script.
- **`cv2.imshow` errors on Colab/headless environments:** live webcam display doesn't work well there — run this locally instead, or process a video file and save the output instead of displaying it live.
- **No webcam detected:** try `VIDEO_SOURCE = 1` instead of `0`, or use a video file.
