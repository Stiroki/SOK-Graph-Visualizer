from datetime import date
from typing import Any, Dict, List, Optional, Union

AttributeValue = Union[int, str, float, date]
ALLOWED_TYPES = (int, str, float, date)


class Node:
    def __init__(self, node_id: str, attributes: Optional[Dict[str, AttributeValue]] = None):
        self.id: str = node_id
        self.attributes: Dict[str, AttributeValue] = {}
        if attributes:
            for key, value in attributes.items():
                self.set_attribute(key, value)

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        if isinstance(value, bool) or not isinstance(value, ALLOWED_TYPES):
            raise TypeError(
                f"Atribut '{key}' ima nedozvoljen tip {type(value).__name__}. "
                f"Dozvoljeni su samo: int, str, float, date."
            )
        self.attributes[key] = value

    def get_attribute(self, key: str) -> Optional[AttributeValue]:
        return self.attributes.get(key)

    def __repr__(self) -> str:
        return f"Node(id={self.id!r}, attributes={self.attributes!r})"


class Edge:
    def __init__(
        self,
        edge_id: str,
        source: Node,
        target: Node,
        directed: bool = True,
        attributes: Optional[Dict[str, AttributeValue]] = None,
    ):
        self.id: str = edge_id
        self.source: Node = source
        self.target: Node = target
        self.directed: bool = directed
        self.attributes: Dict[str, AttributeValue] = {}
        if attributes:
            for key, value in attributes.items():
                self.set_attribute(key, value)

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        if isinstance(value, bool) or not isinstance(value, ALLOWED_TYPES):
            raise TypeError(
                f"Atribut '{key}' ima nedozvoljen tip {type(value).__name__}. "
                f"Dozvoljeni su samo: int, str, float, date."
            )
        self.attributes[key] = value

    def __repr__(self) -> str:
        arrow = "->" if self.directed else "--"
        return f"Edge({self.source.id} {arrow} {self.target.id}, id={self.id!r})"


class Graph:
    def __init__(self, directed: bool = True):
        self.directed: bool = directed
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Čvor sa ID-em '{node.id}' već postoji u grafu.")
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.source.id not in self.nodes or edge.target.id not in self.nodes:
            raise ValueError("Oba čvora grane moraju prethodno postojati u grafu.")
        if edge.id in self.edges:
            raise ValueError(f"Grana sa ID-em '{edge.id}' već postoji u grafu.")
        self.edges[edge.id] = edge

    def get_neighbors(self, node_id: str) -> List[Node]:
        if node_id not in self.nodes:
            raise KeyError(f"Čvor '{node_id}' ne postoji u grafu.")
        neighbors: List[Node] = []
        for edge in self.edges.values():
            if edge.source.id == node_id:
                neighbors.append(edge.target)
            elif not self.directed and edge.target.id == node_id:
                neighbors.append(edge.source)
        return neighbors