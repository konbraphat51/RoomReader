from PIL import Image
from UnityQuaternion import Quaternion
from RoomReader.Vector import Vector
from pathlib import Path


class ImageData:
    def __init__(
        self,
        image: Image,
        quaternion: Quaternion,
        position: Vector,
        path: Path,
    ) -> None:
        self.image = image
        self.quaternion = quaternion
        self.position = position
        self.path = path
        self.width, self.height = image.size
