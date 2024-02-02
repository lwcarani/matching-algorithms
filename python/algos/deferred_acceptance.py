from collections import defaultdict
from typing import Dict, Set, Tuple, List


def employee_without_match(matches: Dict[str, str], employees: Set[str]) -> str:
    """
    Helper function to determine if employee is unmatched.
    Returns the first employee encountered that is not
    yet matched. employees can be matched with a job, or
    themselves. If matched to themselves, this means that the
    matching algorithm has exhausted their entire preference
    list. If all employees are matched, this function will
    return None, and we will break from deferred acceptance algorithm.
    """
    for employee in employees:
        if employee not in matches:
            return employee


def da(
    employee_preferences: Dict[str, List[str]], job_preferences: Dict[str, List[str]]
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Implementation of the deferred acceptance (DA) algorithm (also
    (also as Gale-Shapley algorithm), first published in 1962.
    Iterates through all employees and their preference lists,
    and tentatively assigns them to the most preferred job on
    their list, only re-assigning them if the job they are
    tentatively assigned to is "proposed to" by an employee
    that the job desires more. When this happens, the initial
    employee is bumped (because the job prefers its new offer),
    and then the algorithm iteratively attempts to assign this
    "bumped" employee a remaining job as high on their preference
    list as possible. Algorithm terminates when either (1) all
    employees have been assigned, or (2) all employees have
    exhausted their preference lists (no more jobs available).
    """
    job_queue: Dict = defaultdict(int)
    employees: Set[str] = set(employee_preferences.keys())
    matches: Dict = {}

    while True:
        # get the next available employee that is still unmatched to a job
        employee = employee_without_match(matches, employees)
        # once all employees have been matched (to a job or themselves), employee_without_match function will return
        # a None type object, and we will break from while loop. If an employee is matched to themself it means the
        # algorithm exhausted their preference list (e-Resume), and was not able to match them with any job
        if not employee:
            break

        # queue (counter) to track which job we are currently considering for the current employee
        # i.e., if job_index is 2, then we are considering the 3rd job on the given
        # employee's preference list (0-indexing)
        job_index = job_queue[employee]
        # increment counter so that next time through loop, we consider the next job on the preference list
        # since this is a defaultdict, new entries automatically start at 0
        job_queue[employee] += 1

        # Try to match the current employee with the next available job on their rank ordered list, if available
        if job_index < len(employee_preferences[employee]):
            job = employee_preferences[employee][job_index]
        # if we've gone through the employee's entire list, assign employee to themself to indicate unmatched
        else:
            matches[employee] = employee
            continue

        prev_employee: str | None = matches.get(
            job, None
        )  # check if someone was already assigned to this job

        # if prev_employee is None, then no one has been assigned this job yet,
        # so go ahead and assign to current employee. No swap needs to be made.
        if prev_employee is None:
            matches[employee] = job
            matches[job] = employee

        # otherwise, if prev_employee is not None, then someone is already assigned to that job,
        # check and see who has priority. If the current employee has a higher priority
        # than the previous employee assigned to this job, make the new job assignment.
        # This is the primary tiebreaker.
        elif (
            employee in job_preferences[job]
            and prev_employee in job_preferences[job]
            and job_preferences[job].index(employee)
            < job_preferences[job].index(prev_employee)
        ):
            matches[employee] = job
            matches[job] = employee
            del matches[prev_employee]

    # return two-sided match (employee to job and job to employee), and one-sided match (employee to job)
    return matches, {employee: matches[employee] for employee in employees}
