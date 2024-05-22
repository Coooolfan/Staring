import onnxruntime as ort
import cv2

import sys
from time import time
import numpy as np


#https://microsoft.github.io/onnxruntime/

def pre_proccess(img_bgr):
    # img_path = 'pics/p2.jpg'
    # img_bgr = cv2.imread(img_path)
    ## BGR 转 RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # Resize the image to (640, 640)
    img_rgb_640 = cv2.resize(img_rgb, (640, 640))
    input_tensor = img_rgb_640 / 255
    input_tensor = np.expand_dims(input_tensor, axis=0)  # Add batch dimension
    input_tensor = input_tensor.transpose((0, 3, 1, 2))  # Change shape to N, C, H, W
    input_tensor = np.ascontiguousarray(input_tensor)  # Convert to contiguous array for faster access
    return input_tensor.astype(np.float32)


def proccess(input_tensor):
    return ors.run(None, {"images": input_tensor})[0]


ors = ort.InferenceSession("yolov8n.onnx")
ors.set_providers(["CUDAExecutionProvider"])
inputs = ors.get_inputs()

video_path = "C:/Users/Yang/Desktop/学姐向你发出了约会邀请❤怦然心动❤.1542979357.mp4"
cap = cv2.VideoCapture(video_path)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
total_time = 0
while 1:
    ret, frame = cap.read()
    if not ret:
        break

    frame = pre_proccess(frame)
    start_time = time()
    proccess(frame)
    total_time += time() - start_time

    # 打印进度
    finished_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    sys.stdout.write("\r进度: %.2f %%" % (finished_frames / total_frames * 100))
    sys.stdout.flush()

# 2024-05-22 23:49:47 FPS:  75.26831062457265 GPU
print("\nFPS: ", total_frames / total_time)
