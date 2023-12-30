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
        
        self._to_scatter(df, config).save(config.result_directory / "semantic.html")

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
    
    def _to_scatter(self, df: pd.DataFrame, config: Config) -> alt.Chart:
        selection = alt.selection_multi(fields=['class'], bind='legend')
        color = alt.condition(selection,
                          alt.Color('class:N', title="Class"),
                          alt.value('lightgray'))
        
        x_range = alt.X('x:Q', title="X")
        y_range = alt.Y('y:Q', title="Y")
        
        if config.flag_observer_range:
            # get range
            x_observer_range = [df[df["class"] == "Observe Point"]["x"].min() - config.observer_range_offset, df[df["class"] == "Observe Point"]["x"].max() + config.observer_range_offset]
            y_observer_range = [df[df["class"] == "Observe Point"]["y"].min() - config.observer_range_offset, df[df["class"] == "Observe Point"]["y"].max() + config.observer_range_offset]
            
            x_range = alt.X('x:Q', title="X", scale=alt.Scale(domain=x_observer_range))
            y_range = alt.Y('y:Q', title="Y", scale=alt.Scale(domain=y_observer_range))

            # limit data
            df = df[(df["x"] >= x_observer_range[0]) & (df["x"] <= x_observer_range[1]) & (df["y"] >= y_observer_range[0]) & (df["y"] <= y_observer_range[1])]
        
        return alt.Chart(df).mark_circle(size=60).encode(
            x=x_range,
            y=y_range,
            color=color,
            tooltip=['class']
        ).add_selection(
            selection
        )