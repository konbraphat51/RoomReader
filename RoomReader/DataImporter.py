from __future__ import annotations
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from UnityQuaternion import Quaternion
from RoomReader.Config import Config
from RoomReader.Vector import Vector


class ImageData:
    def __init__(self,
                 image:Image,
                 quaternion: Quaternion,
                 position: Vector
                 ) -> None:
        self.image = image
        self.quaternion = quaternion
        self.position = position

def import_data(config: Config) -> list[ImageData]:
    pass