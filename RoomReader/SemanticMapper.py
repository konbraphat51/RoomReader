from __future__ import annotations
from typing import Iterable
from UnityQuaternion import Quaternion
from RoomReader.DetectionData import DetectionData
from RoomReader.ImageData import ImageData
from RoomReader.Config import Config
from RoomReader.Vector import Vector
from RoomReader.GeometryHelper import get_index, in_room

def map_semantic(detection_data: Iterable[DetectionData], config: Config):
    scaler_fields = create_semantic_fields(detection_data, config)
    
    vector_field = _make_scaler_field(config, "")
    for x in range(len(vector_field)):
        for y in range(len(vector_field[x])):
            for z in range(len(vector_field[x][y])):
                _class_num = {}
                for _class in scaler_fields.keys():
                    _class_num[_class] = scaler_fields[_class][x][y][z]
                    
                max_class = max(_class_num, key=_class_num.get)
                
                if _class_num[max_class] >= config.semantic_threshold:
                    vector_field[x][y][z] = max_class
                    
    return vector_field

def map_semantic_2d(detection_data: Iterable[DetectionData], config: Config):
    scaler_fields = create_semantic_fields(detection_data, config)
    
    vector_field = _make_scaler_field(config, "")
    for x in range(len(vector_field)):
        for y in range(len(vector_field[x])):
            #squeeze z axis
            vector_field[x][y] = ""
            
            _class_num = {}
            for _class in scaler_fields.keys():
                for z in range(len(scaler_fields[_class][x][y])):
                    _class_num[_class] = _class_num.get(_class, 0) + scaler_fields[_class][x][y][z]
                    
            if len(_class_num) == 0:
                continue
            
            max_class = max(_class_num, key=_class_num.get)
                
            if _class_num[max_class] >= config.semantic_threshold:
                vector_field[x][y] = max_class
                    
    return vector_field
        
    
def create_semantic_fields(detection_data: Iterable[DetectionData], config: Config) -> dict[str, list[list[list[float]]]]:
    #make unique classes list
    classes_unique = _make_unique_classes(detection_data)
    
    scaler_fields = {}
    for _class in classes_unique:
        scaler_fields[_class] = _make_scaler_field(config)
        
    for _class in classes_unique:
        filtered_data = _filter_by_class(detection_data, _class)
        scaler_fields[_class] = _weighten_field(filtered_data, config)
        
    return scaler_fields
            
def _make_unique_classes(detection_data: Iterable[DetectionData]):
    class_exists = []
    for detection in detection_data:
        if detection.name not in class_exists:
            class_exists.append(detection.name)
                    
    return class_exists

def _make_scaler_field(config: Config, init=0):
    x_range = int((config.room_x_max - config.room_x_min) / config.interval)
    y_range = int((config.room_y_max - config.room_y_min) / config.interval)
    z_range = int((config.room_z_max - config.room_z_min) / config.interval)
    
    return [[[init for _ in range(z_range)] for _ in range(y_range)] for _ in range(x_range)]

def _weighten_field(detection_data: Iterable[DetectionData], config:Config) -> list[list[list[float]]]:
    output = _make_scaler_field(config)
    
    for detection in detection_data:
        _process_a_detection(output, detection, config)
        
    return output

def _process_a_detection(field: list[list[list[float]]], detection: DetectionData, config: Config):
    device2room = Quaternion.Inverse(detection.image.quaternion)
    direction = device2room * config.camera_vector
    direction = Vector(direction[0], direction[1], direction[2])
    _launch_ray(field, detection.image.position, direction, config)
    
def _launch_ray(field: list[list[list[float]]], start: Vector, direction: Vector, config: Config):
    ray = start
    
    while (in_room(ray, config)):
        field[get_index("x", ray[0], config)][get_index("y", ray[1], config)][get_index("z", ray[2], config)] += 1
        ray += direction * 0.3
    
    return

def _filter_by_class(detection_data: Iterable[DetectionData], _class: str) -> Iterable[DetectionData]:
    return [detection for detection in detection_data if detection.name == _class]
