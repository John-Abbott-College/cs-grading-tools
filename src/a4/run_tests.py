import socket
import os
import sys
import subprocess

"""
Usage:
python run_tests.py <student_submission_folder>

Works on gradescope too.
"""
if __name__ == "__main__":
    if socket.gethostname() == "wsl":
        if len(sys.argv) != 2:
            print("student submission directory needed. Exiting.")
            sys.exit(1)
        prefix = sys.argv[1]
    else:
        prefix = "/autograder"

    if not os.path.isdir(prefix):
        raise FileNotFoundError(f"Testing directory '{prefix}' does not exist")

    # prepare to run the tests
    log_filename = f"{prefix}results.json"
    args = ["python", "-m", 'pytest', "--json-report", "--json-report-indent=2",
            f"--json-report-file={log_filename}", "--json-report-omit", "keywords", "summary", "collectors"]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

