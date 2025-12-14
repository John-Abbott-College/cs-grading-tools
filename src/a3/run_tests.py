import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import socket
import os
import sys

"""
Usage:
python run_tests.py <student_submission_folder>

Works on gradescope too.
"""
if __name__ == "__main__":
    if socket.gethostname() == "home":
        if len(sys.argv) != 2:
            print("student submission directory needed. Exiting.")
            sys.exit(1)
        prefix = sys.argv[1]
    else:
        prefix = "/autograder"

    suite = unittest.defaultTestLoader.discover("tests")
    results_file = f"{prefix}/results.json"

    with open(results_file, "w") as f:
        JSONTestRunner(visibility="visible", stream=f).run(suite)
