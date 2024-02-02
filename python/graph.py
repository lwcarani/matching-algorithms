from typing import Set, Dict, Tuple, Iterable
from node import Node


class Graph(object):
    def __init__(self, node_names: Iterable[str] = []):
        self.nodes: Dict[str, Node] = {name: Node(name) for name in node_names}
        self.edges: Set[Tuple[str, str]] = set()

    def __repr__(self):
        return (
            "Graph(\n  "
            + "\n  ".join(
                [f"{node}: {node.outgoing_edges}" for node in self.nodes.values()]
            )
            + "\n)"
        )

    def add_node(self, name: str):
        self.nodes[name] = Node(name)

    def delete_node(self, node: Node | str):
        if isinstance(node, Node):
            node: str = node.name

        connected_edges = (
            self.nodes[node].incoming_edges | self.nodes[node].outgoing_edges
        )
        for s, t in connected_edges:
            self.nodes[s].outgoing_edges.remove((s, t))
            self.nodes[t].incoming_edges.remove((s, t))
            self.edges.remove((s, t))

        del self.nodes[node]

    def number_of_nodes_in_graph(self) -> int:
        return len(self.nodes)

    def get_random_node(self) -> Node:
        for _, node in self.nodes.items():
            return node

    def add_edge(self, s: str, t: str):
        if s not in self.nodes.keys():
            self.add_node(s)
        if t not in self.nodes.keys():
            self.add_node(t)

        self.nodes[s].outgoing_edges.add((s, t))
        self.nodes[t].incoming_edges.add((s, t))
        self.edges.add((s, t))
