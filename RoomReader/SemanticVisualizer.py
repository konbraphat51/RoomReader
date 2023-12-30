import pandas as pd
import altair as alt
from RoomReader.Config import Config

def visualize_semantic2D(semantic_fields: list[list[str]], config: Config):
    semantic_visualizer = SemanticVisualizer2D()
    semantic_visualizer.visualize(semantic_fields, config)

class SemanticVisualizer:
    pass

class SemanticVisualizer2D(SemanticVisualizer):
    def visualize(self, semantic_fields: list[list[str]], config: Config):
        df = self._convert_to_dataframe(semantic_fields)
        
        self._to_scatter(df).save(config.result_directory / "semantic.html")
    
    def _convert_to_dataframe(self, semantic_fields: list[list[str]]):
        data = []
        for x in range(len(semantic_fields)):
            for y in range(len(semantic_fields[x])):
                if semantic_fields[x][y] == "":
                    continue
                
                data.append({
                    "x": x,
                    "y": y,
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