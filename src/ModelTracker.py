from ultralytics import YOLO
from ultralytics.engine.results import Results


class ModelTracker:
    def __init__(self):
        print("ModelTracker init")
        self.model = YOLO('yolov8n.pt')
        self.model = self.model.to("cpu")
        import torch
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", device)
        # if device.type == "cuda":
        #     self.model = self.model.to(device)

        # self.thread = threading.Thread(target=self.update, args=())
        # self.thread.start()
        print("ModelTracker init end")

    # def update(self):
    #     while self.running:
    #         if self.cap.isOpened():
    #             (self.ret, self.frame) = self.cap.read()

    def track(self, frame) -> Results:
        # Return the latest frame
        return self.model.track(frame, persist=True, verbose=False, half=True, imgsz=320, classes=[0])[0]

    def stop(self):
        # Indicate that the thread should be stopped
        self.model = None
        # self.thread.join()

    def __enter__(self):
        # Making VideoCapture a Context Manager
        return self

    def __exit__(self, exec_type, exc_value, traceback):
        # If any exceptions occur, stop the thread and release the video capture
        self.stop()
