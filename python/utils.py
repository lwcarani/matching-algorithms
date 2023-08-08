from typing import List, Dict

def find_blocking_pairs(
    one_sided_match: Dict[str, str],
    two_sided_match: Dict[str, str],
    employee_preferences: Dict[str, str],
    job_preferences: Dict[str, str]
) -> Dict[str, str]:
    """Return a dictionary of all blocking pairs in final matching, if any exist. A blocking pair in this conext is
    an employee and a job that should've been matched together, because the employee prefers that job more than their 
    current job, and they are more qualified than the employee that was actually assigned. No blocking pairs should
    exist (assuming the algorithm is implemented correctly); this is primarily used for debugging."""
    blocking_pairs = dict()
    for current_employee, job in one_sided_match.items():
        # employee matched with themselves means unmatched, skip to next entry
        if current_employee == job:
            continue
        current_employee_job_rank: int = employee_preferences.get(current_employee).index(job) + 1
        current_employee_prefs: List = employee_preferences.get(current_employee, [])
        # current employee got their number one choice, can't be better off, skip to next entry
        if current_employee_job_rank == 1:
            continue
        else:
            for i in range(0, current_employee_job_rank - 1):
                preferred_job = current_employee_prefs[i]

                # if there is a job ranked higher on current_employee's list that they were unassigned to,
                # and current_employee is qualified, then someone else must have been assigned to that job
                other_employee: str = two_sided_match[preferred_job]

                if (
                    current_employee in job_preferences.get(preferred_job)
                    and other_employee in job_preferences.get(preferred_job)
                    and job_preferences.get(preferred_job).index(current_employee) < job_preferences.get(preferred_job).index(other_employee)
                ):
                    # current_employee should've been assigned over other_employee, something went wrong...
                    blocking_pairs[current_employee] = other_employee
                
    return blocking_pairs