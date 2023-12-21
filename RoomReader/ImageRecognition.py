import torch
import csv

model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)


def detect(image_path): 
    results = model(image_path) 
    df_objects = results.pandas().xyxy[0] 

    return df_objects
