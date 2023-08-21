# standard imports
import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized
from typing import List, Dict
from collections import defaultdict

# custom imports
from algos.da_utils import find_blocking_pairs
from algos.top_trading_cycle import ttc, update_graph, find_cycle
from graph import Graph


class TestTopTradingCycle(TestCase):
    """Test the implementation of the top trading cycle (TTC) algorithm."""

    @parameterized.expand(
        [
            [
                {
                    'e1': ['j2','j3','j4','j5','j6','j1'],
                    'e2': ['j3','j4','j5','j6','j1','j2'],
                    'e3': ['j1','j2','j3','j4','j5','j6'],
                    'e4': ['j5','j6','j1','j2','j3','j4'],
                    'e5': ['j4','j1','j2','j3','j5','j6'],
                    'e6': ['j6','j1','j2','j3','j4','j5'],
                },
                {
                    'j1': ['e1'],
                    'j2': ['e2'],
                    'j3': ['e3'],
                    'j4': ['e4'],
                    'j5': ['e5'],
                    'j6': ['e6'],
                }
            ],
            [
                {
                    'e1': ['j1','j2','j3','j4','j5','j6'],
                    'e2': ['j1','j2','j3','j4','j5','j6'],
                    'e3': ['j1','j2','j3','j4','j5','j6'],
                    'e4': ['j1','j2','j3','j4','j5','j6'],
                    'e5': ['j1','j2','j3','j4','j5','j6'],
                    'e6': ['j1','j2','j3','j4','j5','j6'],
                },
                {
                    'j1': ['e1'],
                    'j2': ['e2'],
                    'j3': ['e3'],
                    'j4': ['e4'],
                    'j5': ['e5'],
                    'j6': ['e6'],
                }
            ],
        ]
    )
    def test_blocking_pairs(
        self,
        employee_preferences: Dict[str, List[str]],
        job_preferences: Dict[str, List[str]]
    ) -> None:
        """Check that the TTC algorithm returns a matching with no blocking pairs."""
        two_sided_match, one_sided_match = ttc(employee_preferences, job_preferences)

        blocking_pairs = find_blocking_pairs(
            one_sided_match, 
            two_sided_match, 
            employee_preferences, 
            job_preferences
        )

        self.assertEqual(
            len(blocking_pairs),
            0,
            f"Blocking pairs should not exist in the final matching! {blocking_pairs}"
        )
        print("Success! No blocking pairs detected.")

    @parameterized.expand(
        [
            [{'e1': ['j1', 'j2'], 'e2': ['j2', 'j1']}, {'j1': ['e2', 'e1'], 'j2': ['e2', 'e1']}],
        ]
    )
    def test_basic_graph_methods(
        self,
        employee_preferences: Dict[str, List[str]],
        job_preferences: Dict[str, List[str]]
    ) -> None:
        """Check that the methods in the Graph class function properly."""
        employees = set(employee_preferences.keys())
        jobs = set(job_preferences.keys())
        all_nodes = employees | jobs
        G = Graph(all_nodes)

        self.assertSetEqual(
            all_nodes,
            set(['e1', 'e2', 'j1', 'j2'])
        )
        self.assertEqual(
            G.number_of_nodes_in_graph(),
            4
        )
        # check assertions after Graph update
        G.delete_node('e1')
        self.assertSetEqual(
            set(G.nodes.keys()),
            set(['e2', 'j1', 'j2'])
        )
        self.assertEqual(
            G.number_of_nodes_in_graph(),
            3
        )
        # add node back in 
        G.add_node('e1')
        
        # add edges
        job_queue: Dict = defaultdict(int)
        employee_queue: Dict = defaultdict(int)
    
        # add edges to build out graph
        for e in employees:
            job_index = job_queue[e]
            G.add_edge(e, employee_preferences[e][job_index])
        for j in jobs:
            employee_index = employee_queue[j]
            G.add_edge(j, job_preferences[j][employee_index])
        self.assertSetEqual(
            G.edges,
            {
                ('e1', 'j1'),
                ('j1', 'e2'),
                ('e2', 'j2'),
                ('j2', 'e2')
            }
        )

        # check next nodes for all current nodes in graph
        self.assertEqual(
            G.nodes['e1'].get_random_next_node(),
            'j1'
        )
        self.assertEqual(
            G.nodes['e2'].get_random_next_node(),
            'j2'
        )
        self.assertEqual(
            G.nodes['j1'].get_random_next_node(),
            'e2'
        )
        self.assertEqual(
            G.nodes['j2'].get_random_next_node(),
            'e2'
        )

        # check degree of incoming and outgoing edges
        self.assertEqual(
            G.nodes['e1'].degree_incoming(),
            0
        )
        self.assertEqual(
            G.nodes['e1'].degree_outgoing(),
            1
        )
        self.assertEqual(
            G.nodes['e2'].degree_incoming(),
            2
        )
        self.assertEqual(
            G.nodes['e2'].degree_outgoing(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_incoming(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_outgoing(),
            1
        )
        self.assertEqual(
            G.nodes['j2'].degree_incoming(),
            1
        )
        self.assertEqual(
            G.nodes['j2'].degree_outgoing(),
            1
        )

        # check degree of incoming and outgoing edges
        # after deleting a node
        G.delete_node('e2')
        self.assertEqual(
            G.nodes['e1'].degree_incoming(),
            0
        )
        self.assertEqual(
            G.nodes['e1'].degree_outgoing(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_incoming(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_outgoing(),
            0
        )
        self.assertEqual(
            G.nodes['j2'].degree_incoming(),
            0
        )
        self.assertEqual(
            G.nodes['j2'].degree_outgoing(),
            0
        )

    @parameterized.expand(
        [
            [{'e1': ['j1', 'j2'], 'e2': ['j2', 'j1']}, {'j1': ['e2', 'e1'], 'j2': ['e2', 'e1']}],
        ]
    )
    def test_find_cycle_in_graph(
        self,
        employee_preferences: Dict[str, List[str]],
        job_preferences: Dict[str, List[str]]
    ) -> None:
        """Check that the find_cycle function works properly."""
        matches: Dict[str, str] = dict()
        employees = set(employee_preferences.keys())
        jobs = set(job_preferences.keys())
        all_nodes = employees | jobs
        G = Graph(all_nodes)

        self.assertSetEqual(
            all_nodes,
            set(['e1', 'e2', 'j1', 'j2'])
        )
        self.assertEqual(
            G.number_of_nodes_in_graph(),
            4
        )
        
        # add edges
        job_queue: Dict = defaultdict(int)
        employee_queue: Dict = defaultdict(int)
    
        # add edges to build out graph
        for e in employees:
            job_index = job_queue[e]
            G.add_edge(e, employee_preferences[e][job_index])
        for j in jobs:
            employee_index = employee_queue[j]
            G.add_edge(j, job_preferences[j][employee_index])

        self.assertSetEqual(
            G.edges,
            {
                ('e1', 'j1'),
                ('j1', 'e2'),
                ('e2', 'j2'),
                ('j2', 'e2')
            }
        )
        
        cycle = find_cycle(G)
        cycle.sort()

        self.assertListEqual(
            cycle,
            ['e2', 'j2']
        )

        for node in cycle:
            if node in employees:
                job: str = G.nodes[node].get_random_next_node()
                matches[node] = job
                matches[job] = node
                G.delete_node(node)
                G.delete_node(job)


        self.assertCountEqual(
            matches['e2'],
            'j2'
        )
        self.assertCountEqual(
            matches['j2'],
            'e2'
        )
        self.assertSetEqual(
            set(G.nodes.keys()),
            set(['e1', 'j1'])
        )
        self.assertEqual(
            G.number_of_nodes_in_graph(),
            2
        )
        self.assertSetEqual(
            G.edges,
            {
                ('e1', 'j1')
            }
        )

    @parameterized.expand(
        [
            [{'e1': ['j1', 'j2'], 'e2': ['j2', 'j1']}, {'j1': ['e2', 'e1'], 'j2': ['e2', 'e1']}],
        ]
    )
    def test_find_cycle_in_graph(
        self,
        employee_preferences: Dict[str, List[str]],
        job_preferences: Dict[str, List[str]]
    ) -> None:
        """Check that the find_cycle function works properly."""
        matches: Dict[str, str] = dict()
        employees = set(employee_preferences.keys())
        jobs = set(job_preferences.keys())
        all_nodes = employees | jobs
        G = Graph(all_nodes)
        
        # add edges
        job_queue: Dict = defaultdict(int)
        employee_queue: Dict = defaultdict(int)
    
        # add edges to build out graph
        for e in employees:
            job_index = job_queue[e]
            G.add_edge(e, employee_preferences[e][job_index])
        for j in jobs:
            employee_index = employee_queue[j]
            G.add_edge(j, job_preferences[j][employee_index])
        
        cycle = find_cycle(G)
        cycle.sort()

        self.assertListEqual(
            cycle,
            ['e2', 'j2']
        )

        for node in cycle:
            if node in employees:
                job: str = G.nodes[node].get_random_next_node()
                matches[node] = job
                matches[job] = node
                G.delete_node(node)
                G.delete_node(job)

        G, matches, employee_queue, job_queue = update_graph(
            G, 
            matches, 
            employee_preferences, 
            job_preferences, 
            employee_queue, 
            job_queue
        )

        self.assertSetEqual(
            G.edges,
            {
                ('e1', 'j1'),
                ('j1', 'e1')
            }
        )
        # check degree of incoming and outgoing edges
        self.assertEqual(
            G.nodes['e1'].degree_incoming(),
            1
        )
        self.assertEqual(
            G.nodes['e1'].degree_outgoing(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_incoming(),
            1
        )
        self.assertEqual(
            G.nodes['j1'].degree_outgoing(),
            1
        )
        self.assertEqual(
            job_queue['e1'],
            0
        )
        self.assertEqual(
            employee_queue['j1'],
            1
        )
        
if __name__ == '__main__':
    unittest.main()
