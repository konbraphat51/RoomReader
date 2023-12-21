from RoomReader.Config import Config
from RoomReader.DataImporter import import_pictures
from ImageRecognition import detect_images

config = Config()
config.data_directory = config.sampledata_directory

images = import_pictures(config)
detection_data = detect_images(images)

print(detection_data)