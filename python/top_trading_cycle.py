# standard imports
from typing import List, Dict, Tuple
from collections import defaultdict

# custom imports
from graph import Graph
from ttc_utils import find_cycle, update_graph


def ttc(
    employee_preferences: Dict[str, List[str]],
    job_preferences: Dict[str, List[str]]
) -> Tuple[Dict[str, str], Dict[str, str]]:
    matches: Dict[str, str] = {}
    employees = set(employee_preferences.keys())
    jobs = set(job_preferences.keys())
    all_nodes = employees | jobs

    # instantiate a new Graph object with all employee and job nodes
    # initially, this graph will only have nodes, no edges
    G = Graph(all_nodes)

    # queue (counter) to track which job we are currently considering for the current employee
    # i.e., if job_index is 2, then we are considering the 3rd job on the given
    job_queue: Dict = defaultdict(int)
    employee_queue: Dict = defaultdict(int)
    
    # add edges to build out graph
    for e in employees:
        job_index = job_queue[e]  # new entries start at 0 for defaultdict
        G.add_edge(e, employee_preferences[e][job_index])
    for j in jobs:
        employee_index = employee_queue[j]  # new entries start at 0 for defaultdict
        G.add_edge(j, job_preferences[j][employee_index])

    # Remove top trading cycles until graph is empty
    while G.number_of_nodes_in_graph() > 0:
        # find an arbitrary cycle in the graph
        cycle = find_cycle(G)

        # make assignments of employees to job based on cycle that was found
        for node in cycle:
            if node in employees:
                job: str = G.nodes[node].get_random_next_node()
                matches[node] = job
                matches[job] = node
                G.delete_node(node)
                G.delete_node(job)

        # update the graph with new edges after cycle was found and matches were made
        G, matches, employee_queue, job_queue = update_graph(
            G, 
            matches, 
            employee_preferences, 
            job_preferences, 
            employee_queue, 
            job_queue
        )

    return matches, {employee: matches[employee] for employee in employees}
