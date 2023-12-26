from __future__ import annotations
from random import random
from pathlib import Path
from PIL import Image
import numpy as np
import torch
from RoomReader.Config import Config
from RoomReader.DetectionData import DetectionData
from RoomReader.ImageData import ImageData

def detect_image(image: ImageData, config: Config) -> list[DetectionData]:
    results = config.yolo_model(image.path.resolve())
    
    _save_detection_image(results, config)
    
    return _to_class_data(results, image)

def detect_images(images: list[ImageData], config: Config) -> list[DetectionData]:
    detections = []
    for image in images:
        detections.extend(detect_image(image, config))

    return detections

def _to_class_data(results, image: ImageData):
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

def _save_detection_image(results, config: Config):
    img_array = results.render()[0]
    
    img = Image.fromarray(img_array)
    
    img.save(config.detection_result_directory / Path(str(int(random()*1000))+".png"))