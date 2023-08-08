# standard imports
from typing import List, Dict, Set
from collections import defaultdict

# custom imports
from graph import Graph, Node


def find_cycle(G: Graph) -> List[str] | None:
    if G.number_of_nodes_in_graph == 0:
        return None
    visited_nodes: Set[str] = set()
    cycle: List[str] = list()
    # start at an arbitrary node in the graph to begin random walk
    # repeat until we find a cycle. NOTE: a cycle is guaranteed to exist.
    n: Node = G.get_random_node()
    while n.name not in visited_nodes:
        visited_nodes.add(n.name)
        cycle.append(n.name)
        n: Node = G.nodes[n.get_random_next_node()]

    start_of_cycle_index = cycle.index(n.name)
    return cycle[start_of_cycle_index:]


def update_graph(
    G, 
    matches, 
    employee_preferences, 
    job_preferences,
    employee_queue,
    job_queue
):
    employees = set(employee_preferences.keys())
    jobs = set(job_preferences.keys())

    for e in employees:
        # if the job that this employee was "pointing" at is no longer available,
        # add an edge between this employee and their next highest job preference
        if e in G.nodes.keys() and G.nodes.get(e).degree_outgoing() == 0:
            # increment counter so that next time through loop, we consider the next job on the preference list
            while True:
                job_queue[e] += 1
                job_index = job_queue[e]
                # add a directed edge from this employee to their next highest preference that is still available
                if job_index < len(employee_preferences[e]):
                    next_job_preference: str = employee_preferences[e][job_index]
                # if we've gone through the employee's entire list, assign employee to themself to indicate unmatched
                # delete them from the graph
                else:
                    matches[e] = e
                    G.delete_node(e)
                    break

                # if this employee's next highest preference has not yet been assigned, add a directed edge
                if next_job_preference not in matches:
                    G.add_edge(e, next_job_preference)
                    break

    for j in jobs:
        # if the employee that this job was "pointing" at is no longer available,
        # add an edge between this job and their next highest employee preference
        if j in G.nodes.keys() and G.nodes.get(j).degree_outgoing() == 0:
            # increment counter so that next time through loop, we consider the next employee on the preference list
            while True:
                employee_queue[j] += 1
                employee_index = employee_queue[j]
                # add a directed edge from this job to their next highest preference that is still available
                if employee_index < len(job_preferences[j]):
                    next_employee_preference: str = job_preferences[j][employee_index]
                # if we've gone through the job's entire list, this job will be unfilled,
                # delete it from the graph
                else: 
                    G.delete_node(j)
                    break
                # if this job's next highest preference has not yet been assigned, add a directed edge
                if next_employee_preference not in matches:
                    G.add_edge(j, next_employee_preference)
                    break
            
    return G, matches, employee_queue, job_queue
        

def ttc(
    employee_preferences: Dict[str, List[str]],
    job_preferences: Dict[str, List[str]]
) -> Dict[str, str]:
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





