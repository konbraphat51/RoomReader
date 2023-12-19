from PIL import Image
from UnityQuaternion import Quaternion
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