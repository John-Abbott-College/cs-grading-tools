import os
import sys
import subprocess

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

    results_file = f"{path}results.json"
    args = [
        "python",
        "-m",
        "pytest",
        "--json-report",
        "--json-report-indent=2",
        f"--json-report-file={results_file}",
        "--json-report-omit",
        "keywords",
        "summary",
        "collectors",
    ]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
