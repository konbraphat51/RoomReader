from __future__ import annotations
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from UnityQuaternion import Quaternion
from RoomReader.Config import Config
from RoomReader.Vector import Vector
from RoomReader.ImageData import ImageData

#find maker note id
for k, v in TAGS.items():
    if v == "MakerNote":
        MAKER_NOTE_ID = k
        break

def import_picture(path: Path, config: Config) -> ImageData:
    """Imports a picture from a given path and returns a ImageData object."""
    image = Image.open(path.resolve())
    
    # Get the exif data
    exif_data = image.getexif()
    
    for k, v in exif_data.items():
        print(f"{TAGS.get(k)}: {v}")
    
    maker_note = exif_data[MAKER_NOTE_ID]
    print(maker_note)
    
    image_data = ImageData(image)
    
    
if __name__ == "__main__":
    import_picture(Path("Data/image_2023-12-19T09-25-18.962Z.jpg"), Config())