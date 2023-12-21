from __future__ import annotations
from pathlib import Path
import json
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
    exif_data = image._getexif()
    maker_note = exif_data[MAKER_NOTE_ID].decode("utf-8")    
    maker_note_json = json.loads(maker_note)
    
    # get position
    position = Vector(maker_note_json["position_x"], maker_note_json["position_y"], maker_note_json["position_z"])
    
    # get direction
    direction = Quaternion(maker_note_json["direction_x"], maker_note_json["direction_y"], maker_note_json["direction_z"], maker_note_json["direction_w"])
    
    image_data = ImageData(image, direction, position)
    
    return image_data

def import_pictures(config: Config) -> list[ImageData]:
    """Imports all pictures from the data directory and returns a list of ImageData objects."""
    image_data_list = []
    
    for path in config.data_directory.iterdir():
        image_data_list.append(import_picture(path, config))
        
    return image_data_list
    