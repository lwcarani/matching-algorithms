# standard imports
import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized
from typing import List, Dict

# custom imports
import data_generator
from da_utils import find_blocking_pairs
from deferred_acceptance import da


class TestDeferredAcceptance(TestCase):
    """Test the implementation of the deferred acceptance (DA) algorithm."""

    @parameterized.expand(
        [
            data_generator.generate_preference_data(100, 100, 10),
            data_generator.generate_preference_data(100, 10, 10),
            data_generator.generate_preference_data(10, 100, 10),
            data_generator.generate_preference_data(100, 100, 5),
            data_generator.generate_preference_data(100, 100, 100),
            data_generator.generate_preference_data(10, 10, 10),
            data_generator.generate_preference_data(5, 5, 5),
            data_generator.generate_preference_data(1000, 500, 50),
            data_generator.generate_preference_data(100, 1000, 50),
            data_generator.generate_preference_data(100, 1000, 5),
            data_generator.generate_preference_data(100, 1000, 25),
            data_generator.generate_preference_data(500, 500, 25),
            data_generator.generate_preference_data(50, 50, 25),
            data_generator.generate_preference_data(5000, 500, 50),
            data_generator.generate_preference_data(3000, 3000, 20),
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
        """Check that the DA algorithm returns a matching with no blocking pairs."""
        two_sided_match, one_sided_match = da(employee_preferences, job_preferences)

        blocking_pairs = find_blocking_pairs(
            one_sided_match, 
            two_sided_match, 
            employee_preferences, 
            job_preferences
        )

        self.assertEqual(
            len(blocking_pairs),
            0,
            "Blocking pairs should not exist in the final matching!"
        )
        print("Success! No blocking pairs detected.")

if __name__ == '__main__':
    unittest.main()
