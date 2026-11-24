from abc import ABC, abstractmethod
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .model import Graph


class Plugin(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:
        pass


class DataSourcePlugin(Plugin):

    @abstractmethod
    def get_required_parameters(self) -> List[str]:
        pass

    @abstractmethod
    def load(self, params: Dict[str, Any]) -> "Graph":
        pass


class VisualizerPlugin(Plugin):
    @abstractmethod
    def render(self, graph: "Graph") -> str:

        pass