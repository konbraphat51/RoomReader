from __future__ import annotations
from typing import Iterable
import math
from UnityQuaternion import Quaternion
from RoomReader.DetectionData import DetectionData
from RoomReader.ImageData import ImageData
from RoomReader.Config import Config
from RoomReader.Vector import Vector
from RoomReader.GeometryHelper import get_index, in_room


def map_semantic(detection_data: Iterable[DetectionData], config: Config):
    semantic_mapper = SemanticMapper()
    return semantic_mapper.map_semantic(detection_data, config)


def map_semantic_2d(detection_data: Iterable[DetectionData], config: Config):
    semantic_mapper = SemanticMapper2D()
    return semantic_mapper.map_semantic(detection_data, config)


# abstract
class SemanticMapper:
    def map_semantic(
        self, detection_data: Iterable[DetectionData], config: Config
    ):
        scaler_fields = self.create_semantic_fields(detection_data, config)

        return self.make_output(scaler_fields, config)

    def make_output(
        self, scaler_fields: dict[str, list[list[list[float]]]], config: Config
    ):
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

    def create_semantic_fields(
        self, detection_data: Iterable[DetectionData], config: Config
    ) -> dict[str, list[list[list[float]]]]:
        # make unique classes list
        classes_unique = _make_unique_classes(detection_data)

        scaler_fields = {}
        for _class in classes_unique:
            scaler_fields[_class] = _make_scaler_field(config)

        # make scaler field seperated by detected classes
        for _class in classes_unique:
            # detection data of only this class
            filtered_detection = _filter_by_class(detection_data, _class)

            scaler_fields[_class] = self._weighten_field(
                filtered_detection, config
            )

        return scaler_fields

    def _weighten_field(
        self, detection_data: Iterable[DetectionData], config: Config
    ) -> list[list[list[float]]]:
        output = _make_scaler_field(config)

        # sort by position
        sorted_detection_data = sorted(
            detection_data, key=lambda detection: detection.position
        )

        # position -> list[DetectionData]
        detections_for_position = [[sorted_detection_data[-1]]]

        # classify by position
        for detection in detection_data:
            # if position is same as last one...
            if detection.position == detections_for_position[-1][0].position:
                # ...add to last (same position) list
                detections_for_position[-1].append(detection)
            # if not...
            else:
                # ...make new list for new position
                detections_for_position.append([detection])

        # get marked boolean field
        for detections in detections_for_position:
            field = _make_scaler_field(config, False)
            for detection in detections:
                self._process_a_detection(field, detection, config)

            # add to output
            for x in range(len(output)):
                for y in range(len(output[x])):
                    for z in range(len(output[x][y])):
                        if field[x][y][z]:
                            output[x][y][z] += 1

        return output

    def _process_a_detection(
        self,
        field: list[list[list[bool]]],
        detection: DetectionData,
        config: Config,
    ):
        # get image direction
        device2room = Quaternion.Inverse(detection.image.quaternion)
        direction = device2room * config.camera_vector
        direction = Vector(direction[0], direction[1], direction[2])

        vectors_launching = []

        # center of detection
        center_in_image = (
            Vector(detection.xmin, detection.ymin, 0)
            + Vector(detection.xmax, detection.ymax, 0)
        ) * 0.5
        center_angle_x, center_angle_y = _get_angle_in_camera(
            center_in_image, detection, config
        )
        center_vector = _vector_rotate_vector_by_incamera_angle(
            direction, center_angle_x, center_angle_y
        )
        vectors_launching.append(center_vector)

        for vector in vectors_launching:
            self._launch_ray(field, detection, vector, config)

    def _launch_ray(
        self,
        field: list[list[list[bool]]],
        detection: DetectionData,
        direction: Vector,
        config: Config,
    ):
        ray_vector = direction * config.ray_interval
        ray_position = detection.image.position.clone()

        while in_room(ray_position, config):
            x, y, z = get_index(ray_position, config)
            field[x][y][z] = True

            ray_position += ray_vector


class SemanticMapper2D(SemanticMapper):
    def make_output(
        self, scaler_fields: dict[str, list[list[list[float]]]], config: Config
    ):
        vector_field = super().make_output(scaler_fields, config)

        # to 2D
        vector_field_2d = []
        for x in range(len(vector_field)):
            vector_field_2d.append([])
            for y in range(len(vector_field[x])):
                vector_field_2d[x].append(vector_field[x][y][0])

        return vector_field_2d

    def _launch_ray(
        self,
        field: list[list[list[bool]]],
        detection: DetectionData,
        direction: Vector,
        config: Config,
    ):
        ray_vector = direction * config.ray_interval
        ray_position = detection.image.position.clone()

        while in_room(ray_position, config):
            x, y, z = get_index(ray_position, config)
            field[x][y][0] = True

            ray_position += ray_vector


def _get_angle_in_camera(
    point: Vector, detection: DetectionData, config: Config
) -> Vector:
    # x in camera
    center_x = point[0]
    if center_x > detection.image.width * 0.5:
        # center is in right side of image
        ratio = (center_x - detection.image.width * 0.5) / (
            detection.image.width * 0.5
        )
        angle_x = _get_angle_from_ratio(ratio, config.angle_of_view_x)
    else:
        # center is in left side of image
        ratio = (detection.image.width * 0.5 - center_x) / (
            detection.image.width * 0.5
        )
        angle_x = -_get_angle_from_ratio(ratio, config.angle_of_view_x)

    # y in camera
    center_y = point[1]
    if center_y > detection.image.height * 0.5:
        # center is in bottom side of image
        ratio = (center_y - detection.image.height * 0.5) / (
            detection.image.height * 0.5
        )
        angle_y = _get_angle_from_ratio(ratio, config.angle_of_view_y)
    else:
        # center is in top side of image
        ratio = (detection.image.height * 0.5 - center_y) / (
            detection.image.height * 0.5
        )
        angle_y = -_get_angle_from_ratio(ratio, config.angle_of_view_y)

    return Vector(angle_x, angle_y, 0)


def _get_angle_from_ratio(ratio: float, camera_angle_of_view: float):
    # https://github.com/konbraphat51/ReckonerCamera/issues/1#issuecomment-1869883039
    return math.acos(
        ratio * math.cos(math.radians(camera_angle_of_view * 0.5))
    )


def _vector_rotate_vector_by_incamera_angle(
    vector: Vector, camera_angle_x: float, camera_angle_y: float
) -> Vector:
    # rotate by x angle
    vector = (
        Quaternion.Euler(0, 0, -camera_angle_x) * vector
    )  # negating for left-threated coordinate system
    vector = Vector(vector[0], vector[1], vector[2])

    # rotate by y angle
    rotate_axis = Vector.cross(vector, Vector(0, 0, 1))
    vector = Quaternion.AngleAxis(camera_angle_y, rotate_axis) * vector

    return vector


def _filter_by_class(
    detection_data: Iterable[DetectionData], _class: str
) -> Iterable[DetectionData]:
    return [
        detection for detection in detection_data if detection.name == _class
    ]


def _make_unique_classes(detection_data: Iterable[DetectionData]):
    class_exists = []
    for detection in detection_data:
        if detection.name not in class_exists:
            class_exists.append(detection.name)

    return class_exists


def _make_scaler_field(config: Config, init=0) -> list[list[list[any]]]:
    x_range = int((config.room_x_max - config.room_x_min) / config.interval)
    y_range = int((config.room_y_max - config.room_y_min) / config.interval)
    z_range = int((config.room_z_max - config.room_z_min) / config.interval)

    return [
        [[init for _ in range(z_range)] for _ in range(y_range)]
        for _ in range(x_range)
    ]
