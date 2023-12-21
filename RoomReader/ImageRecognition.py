import torch
from RoomReader.DetectionData import DetectionData

model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

def detect_image(image_path: str) -> list[DetectionData]:
    results = model(image_path)
    df_objects = results.pandas().xyxy[0]

    detections = []
    for index, row in df_objects.iterrows():
        xmin = row["xmin"]
        ymin = row["ymin"]
        xmax = row["xmax"]
        ymax = row["ymax"]
        name = row["name"]

        detections.append(DetectionData(xmin, ymin, xmax, ymax, name))

    return detections

def detect_images(image_paths: list[str]) -> list[DetectionData]:
    detections = []
    for image_path in image_paths:
        detections.extend(detect_image(image_path))

    return detections
