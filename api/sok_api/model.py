from datetime import date, datetime
from typing import Dict, List, Optional, Union

AttributeValue = Union[int, str, float, date]
ALLOWED_ATTRIBUTE_TYPES = (int, str, float, date)


def validate_attribute_value(key: str, value: AttributeValue) -> AttributeValue:
    if isinstance(value, bool):
        raise TypeError(f"Atribut '{key}' ne može biti tipa bool.")
    if isinstance(value, datetime):
        return value.date()
    if not isinstance(value, ALLOWED_ATTRIBUTE_TYPES):
        raise TypeError(
            f"Atribut '{key}' ima nedozvoljen tip '{type(value).__name__}'. "
            f"Dozvoljeni tipovi su: int, str, float, date."
        )
    return value


class Node:
    """Predstavlja čvor grafa sa jedinstvenim ID-em i tipiziranim atributima."""

    def __init__(self, node_id: str, attributes: Optional[Dict[str, AttributeValue]] = None):
        if not node_id or not isinstance(node_id, str):
            raise ValueError("ID čvora mora biti neprazan string.")
        self.id: str = node_id
        self.attributes: Dict[str, AttributeValue] = {}
        if attributes:
            for key, value in attributes.items():
                self.set_attribute(key, value)

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        if not key or not isinstance(key, str):
            raise ValueError("Naziv atributa mora biti neprazan string.")
        self.attributes[key] = validate_attribute_value(key, value)

    def get_attribute(self, key: str) -> Optional[AttributeValue]:
        return self.attributes.get(key)

    def remove_attribute(self, key: str) -> None:
        self.attributes.pop(key, None)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

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
        if not edge_id or not isinstance(edge_id, str):
            raise ValueError("ID grane mora biti neprazan string.")
        self.id: str = edge_id
        self.source: Node = source
        self.target: Node = target
        self.directed: bool = directed
        self.attributes: Dict[str, AttributeValue] = {}
        if attributes:
            for key, value in attributes.items():
                self.set_attribute(key, value)

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        if not key or not isinstance(key, str):
            raise ValueError("Naziv atributa mora biti neprazan string.")
        self.attributes[key] = validate_attribute_value(key, value)

    def get_attribute(self, key: str) -> Optional[AttributeValue]:
        return self.attributes.get(key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        arrow = "->" if self.directed else "--"
        return f"Edge(id={self.id!r}, {self.source.id} {arrow} {self.target.id})"


class Graph:
    """
    Generički model grafa koji podržava usmerene, neusmerene,
    povezane, nepovezane, ciklične i aciklične strukture.
    """

    def __init__(self, directed: bool = True):
        self.directed: bool = directed
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Čvor sa ID-em '{node.id}' već postoji u grafu.")
        self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise KeyError(f"Čvor '{node_id}' ne postoji u grafu.")
        if self.get_incident_edges(node_id):
            raise ValueError(
                f"Čvor '{node_id}' ne može biti obrisan jer je povezan sa postojećim granama."
            )
        del self.nodes[node_id]

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def add_edge(self, edge: Edge) -> None:
        if edge.source.id not in self.nodes or edge.target.id not in self.nodes:
            raise ValueError("Izvorišni i odredišni čvor moraju prethodno postojati u grafu.")
        if edge.id in self.edges:
            raise ValueError(f"Grana sa ID-em '{edge.id}' već postoji u grafu.")
        edge.directed = self.directed
        self.edges[edge.id] = edge

    def remove_edge(self, edge_id: str) -> None:
        if edge_id not in self.edges:
            raise KeyError(f"Grana '{edge_id}' ne postoji u grafu.")
        del self.edges[edge_id]

    def get_incident_edges(self, node_id: str) -> List[Edge]:
        """Vraća sve grane koje ulaze u čvor ili izlaze iz njega."""
        return [
            edge
            for edge in self.edges.values()
            if edge.source.id == node_id or edge.target.id == node_id
        ]

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

    def has_cycle(self) -> bool:
        visited = set()

        if self.directed:
            rec_stack = set()

            def dfs_directed(u_id: str) -> bool:
                visited.add(u_id)
                rec_stack.add(u_id)
                for neighbor in self.get_neighbors(u_id):
                    if neighbor.id not in visited:
                        if dfs_directed(neighbor.id):
                            return True
                    elif neighbor.id in rec_stack:
                        return True
                rec_stack.remove(u_id)
                return False

            for node_id in self.nodes:
                if node_id not in visited:
                    if dfs_directed(node_id):
                        return True
            return False
        else:
            def dfs_undirected(u_id: str, parent_id: Optional[str]) -> bool:
                visited.add(u_id)
                for neighbor in self.get_neighbors(u_id):
                    if neighbor.id not in visited:
                        if dfs_undirected(neighbor.id, u_id):
                            return True
                    elif neighbor.id != parent_id:
                        return True
                return False

            for node_id in self.nodes:
                if node_id not in visited:
                    if dfs_undirected(node_id, None):
                        return True
            return False

    def __repr__(self) -> str:
        return f"Graph(directed={self.directed}, nodes={len(self.nodes)}, edges={len(self.edges)})"