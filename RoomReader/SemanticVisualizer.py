from typing import Iterable
from copy import deepcopy
import pandas as pd
import altair as alt
from RoomReader.Config import Config
from RoomReader.DetectionData import DetectionData
from RoomReader.GeometryHelper import from_index, get_index, in_room

def visualize_semantic2D(semantic_fields: list[list[str]], detections: Iterable[DetectionData], config: Config):
    semantic_visualizer = SemanticVisualizer2D()
    semantic_visualizer.visualize(semantic_fields, detections, config)

class SemanticVisualizer:
    def visualize(self, semantic_fields: list[list[str]], detections: Iterable[DetectionData], config: Config):
        df = self._convert_to_dataframe(semantic_fields, detections, config)
        
        self._to_scatter(df).save(config.result_directory / "semantic.html")

class SemanticVisualizer2D(SemanticVisualizer):
    def _convert_to_dataframe(self, semantic_fields: list[list[str]], detections: Iterable[DetectionData], config: Config):
        semantic_fields = deepcopy(semantic_fields)
        
        for detection in detections:
            if not in_room(detection.image.position, config):
                continue
            
            x = get_index("x", detection.image.position[0], config)
            y = get_index("y", detection.image.position[1], config)
            
            semantic_fields[x][y] = "Observe Point"
        
        data = []
        for x in range(len(semantic_fields)):
            for y in range(len(semantic_fields[x])):
                if semantic_fields[x][y] == "":
                    continue
                
                data.append({
                    "x": from_index("x", x, config),
                    "y": from_index("y", y, config),
                    "class": semantic_fields[x][y]
                })
                
        return pd.DataFrame(data)
    
    def _to_scatter(self, df: pd.DataFrame) -> alt.Chart:
        selection = alt.selection_multi(fields=['class'], bind='legend')
        color = alt.condition(selection,
                          alt.Color('class:N', title="Class"),
                          alt.value('lightgray'))
        
        return alt.Chart(df).mark_circle(size=60).encode(
            x=alt.X('x:Q', title="X"),
            y=alt.Y('y:Q', title="Y"),
            color=color,
            tooltip=['class']
        ).add_selection(
            selection
        )