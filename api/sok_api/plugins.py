from abc import ABC, abstractmethod
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .model import Graph


class Plugin(ABC):
    """Bazni apstraktni interfejs za sve plugine u sistemu."""

    @abstractmethod
    def name(self) -> str:
        """Vraća čitljiv naziv plugina za prikaz korisniku."""
        pass

    @abstractmethod
    def identifier(self) -> str:
        """Vraća jedinstveni programski identifikator plugina."""
        pass


class DataSourcePlugin(Plugin):
    """Apstraktni interfejs za plugine koji učitavaju podatke i formiraju graf."""

    @abstractmethod
    def get_required_parameters(self) -> List[str]:
        """Vraća listu obaveznih ulaznih parametara (npr. ['file_path'])."""
        pass

    @abstractmethod
    def load(self, params: Dict[str, Any]) -> "Graph":
        """
        Parsira izvor podataka na osnovu prosleđenih parametara
        i vraća instancu klase Graph.
        """
        pass


class VisualizerPlugin(Plugin):
    """Apstraktni interfejs za plugine koji vizualizuju graf u HTML formatu."""

    @abstractmethod
    def render(self, graph: "Graph") -> str:
        """
        Generiše i vraća string reprezentaciju HTML/SVG elemenata
        koji predstavljaju prosleđeni graf.
        """
        pass