from pathlib import Path
import torch

class Config:
    def __init__(self) -> None:
        self.library_directory = Path(__file__).parent
        self.data_directory = self.library_directory / Path("Data")
        self.sampledata_directory = self.library_directory / Path("SampleData")
        self.yolo_model = model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)