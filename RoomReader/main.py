from RoomReader.Config import Config
from RoomReader.DataImporter import import_pictures
from RoomReader.ImageRecognition import detect_images
from RoomReader.SamplingVisualizer import visualize_sampling
from RoomReader.SemanticMapper import map_semantic, map_semantic_2d

config = Config()
config.data_directory = config.sampledata_directory

images = import_pictures(config)
detection_data = detect_images(images, config)

visualize_sampling(images, config)

semantic_fields = map_semantic_2d(detection_data, config)

output = ""
for row in semantic_fields:
    output += ",".join(row) + "\n"

print(output)