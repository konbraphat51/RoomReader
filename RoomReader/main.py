from RoomReader.Config import Config
from RoomReader.DataImporter import import_pictures
from RoomReader.ImageRecognition import detect_images
from RoomReader.SamplingVisualizer import visualize_sampling
from RoomReader.SemanticMapper import map_semantic, map_semantic_2d
from RoomReader.SemanticVisualizer import visualize_semantic2D

config = Config()
config.data_directory = config.sampledata_directory

images = import_pictures(config)
detection_data = detect_images(images, config)

visualize_sampling(images, config)

semantic_fields = map_semantic_2d(detection_data, config)

visualize_semantic2D(semantic_fields, config)