from __future__ import annotations
import torch
from RoomReader.DetectionData import DetectionData
from RoomReader.ImageData import ImageData

model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

def detect_image(image: ImageData) -> list[DetectionData]:
    results = model(image.path.resolve())
    df_objects = results.pandas().xyxy[0]

    detections = []
    for index, row in df_objects.iterrows():
        xmin = row["xmin"]
        ymin = row["ymin"]
        xmax = row["xmax"]
        ymax = row["ymax"]
        name = row["name"]

        detections.append(DetectionData(image, xmin, ymin, xmax, ymax, name))

    return detections

def detect_images(images: list[ImageData]) -> list[DetectionData]:
    detections = []
    for image in images:
        detections.extend(detect_image(image))

    return detections
