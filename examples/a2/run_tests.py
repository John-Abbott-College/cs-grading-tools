import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import socket
import os
import sys
from pathlib import Path

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

    print(f"{path}")
    Path(f"{path}results.json").touch()

