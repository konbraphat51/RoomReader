from pathlib import Path
import torch
from RoomReader.Vector import Vector


class Config:
    def __init__(self) -> None:
        self.library_directory = Path(__file__).parent
        self.data_directory = self.library_directory / Path("Data")
        self.sampledata_directory = self.library_directory / Path("SampleData")
        self.yolo_model = torch.hub.load(
            "ultralytics/yolov5", "yolov5s", pretrained=True
        )
        self.room_x_min = -5
        self.room_x_max = 20
        self.room_y_min = -5
        self.room_y_max = 20
        self.room_z_min = -20
        self.room_z_max = 20
        self.interval = 0.5
        self.ray_interval = 0.5
        self.semantic_threshold = 2
        self.detection_result_directory = self.library_directory / Path(
            "DetectionResult"
        )
        self.result_directory = self.library_directory / Path("Result")
        self.camera_vector = Vector(0, 0, -1)
        self.save_detection_images = True
        self.angle_of_view_x = 60  # degree
        self.angle_of_view_y = 75  # degree
        self.flag_observer_range = True
        self.observer_range_offset = 3.0
