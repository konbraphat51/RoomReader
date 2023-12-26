from __future__ import annotations
import torch
from RoomReader.Config import Config
from RoomReader.DetectionData import DetectionData
from RoomReader.ImageData import ImageData

def detect_image(image: ImageData, config: Config) -> list[DetectionData]:
    results = config.yolo_model(image.path.resolve())
    
    return _to_class_data(results)

def detect_images(images: list[ImageData], config: Config) -> list[DetectionData]:
    detections = []
    for image in images:
        detections.extend(detect_image(image, config))

    return detections

def _to_class_data(results):
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