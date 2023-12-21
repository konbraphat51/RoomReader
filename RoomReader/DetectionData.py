from RoomReader.ImageData import ImageData


class DetectionData:
    def __init__(
        self,
        image: ImageData,
        xmin: float,
        ymin: float,
        xmax: float,
        ymax: float,
        name: str,
    ):
        self.image = image
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.name = name
