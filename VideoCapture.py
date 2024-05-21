import cv2
import threading


class VideoCapture:
    def __init__(self, index=0):
        print("VideoCapture init")
        self.index = index
        self.cap = cv2.VideoCapture(self.index)
        self.ret, self.frame = self.cap.read()
        self.running = True

        # Start the thread to read frames from the video stream
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        print("VideoCapture init end")

    def update(self):
        # Read the next frame from the stream in a different thread
        while self.running:
            if self.cap.isOpened():
                (self.ret, self.frame) = self.cap.read()

    def read(self):
        # Return the latest frame
        if not self.running:
            self.start()
        return self.ret, self.frame

    def stop(self):
        # Indicate that the thread should be stopped
        self.running = False
        self.thread.join()
        self.cap.release()

    def start(self):
        self.cap = cv2.VideoCapture(self.index)
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def __enter__(self):
        # Making VideoCapture a Context Manager
        return self

    def __exit__(self, exec_type, exc_value, traceback):
        # If any exceptions occur, stop the thread and release the video capture
        self.stop()
        self.cap.release()
