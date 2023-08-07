# standard imports
from typing import List, Dict, Tuple
from numpy.random import default_rng
rng = default_rng()

def generate_preference_data(
    number_of_jobs: int,
    number_of_employees: int,
    job_list_length: int
) -> Tuple[Dict[str, List[str]], dict[str, List[str]]]:
    make_random_list_of_jobs = lambda: ['j' + str(job) for job in rng.choice(range(1, number_of_jobs + 1), job_list_length, replace=False)]
    make_random_list_of_employees = lambda: ['e' + str(employee) for employee in rng.choice(range(1, number_of_employees + 1), number_of_employees, replace=False)]
    employee_preferences: Dict[str, List[str]] = {
        'e' + str(employee): make_random_list_of_jobs() for employee in list(range(1, number_of_employees + 1))
    }
    job_preferences: Dict[str, List[str]] = {
        'j' + str(job): make_random_list_of_employees() for job in list(range(1, number_of_jobs + 1))
    }

    return employee_preferences, job_preferences
