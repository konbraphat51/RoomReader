from pathlib import Path
import torch

class Config:
    def __init__(self) -> None:
        self.library_directory = Path(__file__).parent
        self.data_directory = self.library_directory / Path("Data")
        self.sampledata_directory = self.library_directory / Path("SampleData")
        self.yolo_model = model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        self.room_x_min = -20
        self.room_x_max = 20
        self.room_y_min = -20
        self.room_y_max = 20
        self.room_z_min = -20
        self.room_z_max = 20
        self.interval = 1
        self.semantic_threshold = 2
        self.detection_result_directory = self.library_directory / Path("DetectionResult")