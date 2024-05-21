import time

import cv2

from VideoCapture import VideoCapture
from src.ModelTracker import ModelTracker
from utils import sysState

if __name__ == '__main__':
    time.sleep(0.2)
    tracked_Id = -1
    tracker = ModelTracker()
    cap = VideoCapture(0)
    while (1):
        if sysState.is_locked():
            continue
        _, frame = cap.read()
        results = tracker.track(frame)
        cv2.imshow("YOLOv8 Tracking", results.plot())

        boxes = results.boxes
        # print("person:" + str(len(results)))

        if len(boxes) == 1 and tracked_Id == -1 and boxes[0].is_track:
            tracked_Id = int(boxes[0].id)
            print("tracked_Id:" + str(tracked_Id))

        left = True
        if tracked_Id != -1 and len(boxes) > 0:
            for box in boxes:
                if box.is_track and int(box.id) == tracked_Id:
                    left = False
                    break
        if left and tracked_Id != -1:
            print("left")
            tracked_Id = -1
            sysState.lock()
            cap.stop()


        # key = input()
        # Display the annotated frame

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.stop()
    tracker.stop()
    cv2.destroyAllWindows()
