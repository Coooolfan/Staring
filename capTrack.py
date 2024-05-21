import sys
from collections import defaultdict
from time import time

import cv2
import numpy as np
import torch

from ultralytics import YOLO

from VideoCapture import VideoCapture

# Load the YOLOv8 model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
model = YOLO('yolov8n.pt')
# 如果有可用的GPU，将模型移动到GPU
if device.type == "cuda":
    model = model.to(device)
# Open the video file
video_path = "C:/Users/Yang/Desktop/学姐向你发出了约会邀请❤怦然心动❤.1542979357.mp4"

cap = VideoCapture(0)

# Store the track history
track_history = defaultdict(lambda :[])

# Loop through the video frames
while 1:
    start_time = time()

    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, verbose=False, half=True,imgsz=320)
        print(results[0])
        if results[0].boxes.id is None:
            continue
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cuda()
        track_ids = results[0].boxes.id.int().cuda().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 30:  # retain 90 tracks for 90 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

    fps = 1 / (time() - start_time)
    sys.stdout.write("\rfps: %.2f" % fps)
    sys.stdout.flush()


# Release the video capture object and close the display window
cv2.destroyAllWindows()