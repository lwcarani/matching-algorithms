from typing import Set, Tuple


class Node(object):
    def __init__(self, name: str):
        self.name: str = name
        self.incoming_edges: Set[Tuple[str, str]] = set()
        self.outgoing_edges: Set[Tuple[str, str]] = set()

    def __repr__(self):
        return f"Node({self.name})"
    
    def get_random_next_node(self) -> str:
        return list(self.outgoing_edges)[0][1]
    
    def degree_outgoing(self) -> int:
        return len(self.outgoing_edges)
    
    def degree_incoming(self) -> int:
        return len(self.incoming_edges)