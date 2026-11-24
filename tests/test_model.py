import unittest
from datetime import date
from sok_api.model import Edge, Graph, Node


class TestGraphModel(unittest.TestCase):
    def test_valid_attribute_types(self):
        dob = date(2005, 5, 15)
        node = Node(
            "n1",
            {
                "name": "Pera",
                "age": 21,
                "gpa": 9.2,
                "birth_date": dob,
            },
        )
        self.assertIsInstance(node.get_attribute("name"), str)
        self.assertIsInstance(node.get_attribute("age"), int)
        self.assertIsInstance(node.get_attribute("gpa"), float)
        self.assertIsInstance(node.get_attribute("birth_date"), date)

    def test_invalid_attribute_types_raise_type_error(self):
        with self.assertRaises(TypeError):
            Node("n1", {"is_active": True})

        with self.assertRaises(TypeError):
            Node("n2", {"tags": ["a", "b"]})

        n1 = Node("n1")
        n2 = Node("n2")
        with self.assertRaises(TypeError):
            Edge("e1", n1, n2, attributes={"meta": {"nested": 1}})

    def test_directed_acyclic_graph(self):
        g = Graph(directed=True)
        n1 = Node("1", {"label": "Root"})
        n2 = Node("2", {"label": "Child1"})
        n3 = Node("3", {"label": "Child2"})
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)

        g.add_edge(Edge("e1", n1, n2, directed=True))
        g.add_edge(Edge("e2", n1, n3, directed=True))

        self.assertEqual([n.id for n in g.get_neighbors("1")], ["2", "3"])
        self.assertEqual(g.get_neighbors("2"), [])

    def test_undirected_graph_neighbors(self):
        g = Graph(directed=False)
        n1 = Node("A")
        n2 = Node("B")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge("e1", n1, n2, directed=False))

        self.assertEqual([n.id for n in g.get_neighbors("A")], ["B"])
        self.assertEqual([n.id for n in g.get_neighbors("B")], ["A"])

    def test_cyclic_graph_and_self_loop(self):
        g = Graph(directed=True)
        n1 = Node("1")
        n2 = Node("2")
        g.add_node(n1)
        g.add_node(n2)

        # Ciklus 1 -> 2 -> 1 i self-loop 1 -> 1
        g.add_edge(Edge("e1", n1, n2, directed=True))
        g.add_edge(Edge("e2", n2, n1, directed=True))
        g.add_edge(Edge("e3", n1, n1, directed=True))

        self.assertEqual(len(g.edges), 3)
        self.assertEqual([n.id for n in g.get_neighbors("1")], ["2", "1"])
        self.assertEqual([n.id for n in g.get_neighbors("2")], ["1"])

    def test_disconnected_graph(self):
        g = Graph(directed=True)
        n1 = Node("1")
        n2 = Node("2")
        isolated = Node("3", {"status": "isolated"})
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(isolated)
        g.add_edge(Edge("e1", n1, n2))

        self.assertEqual(len(g.nodes), 3)
        self.assertEqual(g.get_neighbors("3"), [])

    def test_duplicate_ids_and_missing_nodes(self):
        g = Graph()
        n1 = Node("1")
        n2 = Node("2")
        g.add_node(n1)

        with self.assertRaises(ValueError):
            g.add_node(Node("1"))

        with self.assertRaises(ValueError):
            g.add_edge(Edge("e1", n1, n2))  # n2 nije dodat u graf

        g.add_node(n2)
        g.add_edge(Edge("e1", n1, n2))
        with self.assertRaises(ValueError):
            g.add_edge(Edge("e1", n2, n1))  # duplikat ID-a grane

    def test_create_subgraph(self):
        g = Graph(directed=True)
        n1 = Node("1", {"age": 20})
        n2 = Node("2", {"age": 30})
        n3 = Node("3", {"age": 40})
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)

        g.add_edge(Edge("e12", n1, n2))
        g.add_edge(Edge("e23", n2, n3))

        sub = g.create_subgraph(["1", "2"])
        self.assertEqual(set(sub.nodes.keys()), {"1", "2"})
        self.assertEqual(set(sub.edges.keys()), {"e12"})
        sub.nodes["1"].set_attribute("age", 99)
        self.assertEqual(g.nodes["1"].get_attribute("age"), 20)


if __name__ == "__main__":
    unittest.main()