from importlib.metadata import entry_points
from typing import List
from api.sok_api import DataSourcePlugin, VisualizerPlugin, Graph

DATASOURCE_GROUP = "sok.datasource"
VISUALIZER_GROUP = "sok.visualizer"

class PlatformService:
    def __init__(self):
        self.data_sources: List[DataSourcePlugin] = []
        self.visualizers: List[VisualizerPlugin] = []
        self.current_graph: Graph | None = None

    def load_plugins(self):
        self.data_sources = []
        self.visualizers = []
        for ep in entry_points(group=DATASOURCE_GROUP):
            plugin_class = ep.load()
            plugin: DataSourcePlugin = plugin_class()
            self.data_sources.append(plugin)
        for ep in entry_points(group=VISUALIZER_GROUP):
            plugin_class = ep.load()
            plugin: VisualizerPlugin = plugin_class()
            self.visualizers.append(plugin)
