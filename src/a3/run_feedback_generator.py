from datetime import datetime

from grading import Grading
from feedback_utils import get_student_info_from_lea, give_feedback, Student
from check_util import errors_and_warnings
import os
import sys
import json

files = ["my_functions.py", "assignment3.py"]
due_date = datetime(2025, 11, 12, 1)

# ===============================================================================
# ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("student submission directory needed. Exiting.")
        sys.exit(1)
    path = sys.argv[1]

    pathname = os.path.abspath(path)
    dirs = pathname.split(os.sep)

    manual_grading_answers = f"{path}test_answers.txt"
    grading = Grading.de_serialize(manual_grading_answers)

    # Put autograded results in Grading object
    autograding_answers = f"{path}results.json"
    with open(autograding_answers, mode="r") as f:
        autograder_results = json.load(f)

    for test in autograder_results["tests"]:
        test_section = grading.add_section(test["name"], 1)
        test_section.add_result_with_partial_grade(
            test.get("output",""), test["score"], test["max_score"])
        )

    # TODO: pull weights from file
    weights = {}
    for section in grading.sections():
        section.weight = weights.get(section.name, 1)

    student: Student = get_student_info_from_lea(dirs[-1], due_date)
    grading.days_late = student.days_late

    give_feedback(student, grading, files, path)
