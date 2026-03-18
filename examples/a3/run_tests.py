import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import os
import sys

"""
Usage:
python run_tests.py <student_submission_folder>
"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("student submission directory needed. Exiting.")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("student submission directory needed. Exiting.")
        sys.exit(1)

    suite = unittest.defaultTestLoader.discover("tests")
    results_file = f"{path}/results.json"

    with open(results_file, "w") as f:
        JSONTestRunner(visibility="visible", stream=f).run(suite)
