from abc import ABC, abstractmethod
from typing import Any, Dict, List
from .model import Graph


class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """Vraća čitljiv naziv plugina za prikaz korisniku."""
        pass

    @abstractmethod
    def identifier(self) -> str:
        """Vraća jedinstveni identifikator plugina."""
        pass


class DataSourcePlugin(Plugin):
    @abstractmethod
    def get_required_parameters(self) -> List[str]:
        """Vraća listu naziva obaveznih ulaznih parametara (npr. ['file_path'])."""
        pass

    @abstractmethod
    def load(self, params: Dict[str, Any]) -> Graph:
        """Parsira izvor podataka na osnovu prosleđenih parametara i vraća Graph."""
        pass


class VisualizerPlugin(Plugin):
    @abstractmethod
    def render(self, graph: Graph) -> str:
        """Na osnovu modela grafa generiše i vraća HTML string."""
        pass