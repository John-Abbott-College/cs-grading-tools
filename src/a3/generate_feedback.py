from datetime import datetime

from grading import Grading
from feedback_utils import get_student_info_from_lea, give_feedback, Student
from check_util import errors_and_warnings
import os
import sys
import json

files = ["my_functions.py", "assignment3.py"]

# ===============================================================================
# if test_answers.txt is not found, then ask the questions
# ===============================================================================
manual_test_results = dict()

grading = Grading()


def run_manual_tests(autograding_answers):
    section_edits_required = grading.add_section("Submission issues", 1)
    section_coding_quality = grading.add_section("Code quality", 1)
    section_well_tested = grading.add_section("assignment3.py file used correctly", 1)
    section_functionality = grading.add_section("Required functionality", 16)

    # Edits required
    section_edits_required.ask_question_with_partial_grade("no major edits required to get the code to work properly", 1)

    # Coding quality
    section_coding_quality.ask_question_with_partial_grade("variables used appropriately", 1)

    # assignment3.py
    section_well_tested.ask_question_with_partial_grade("assignment3.py used to test the my_functions.py functions", 1)

    # Parse autograder for required functionality
    with open(autograding_answers, mode="r") as f:
        autograder_results = json.load(f)

    for test in autograder_results["tests"]:
        section_functionality.add_result_with_partial_grade(
            test["name"], test["score"], test["max_score"], test.get("output", "")
        )




# ===============================================================================
# ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("student submission directory needed. Exiting.")
        sys.exit(1)
    path = sys.argv[1]

    due_date = datetime(2025, 11, 12, 1)

    pathname = os.path.abspath(path)
    dirs = pathname.split(os.sep)

    manual_grading_answers = f"{path}test_answers.txt"
    autograding_answers = f"{path}results.json"

    if not os.path.exists(manual_grading_answers):
        run_manual_tests(autograding_answers)
        with open(manual_grading_answers, "w", encoding="utf-8") as fh:
            print(str(grading), file=fh)

    else:
        ans = input("Do you want to re-answer questions? ")
        if "y" in ans:
            run_manual_tests(autograding_answers)
            with open(manual_grading_answers, "w", encoding="utf-8") as fh:
                print(str(grading), file=fh)

    grading = Grading.de_serialize(manual_grading_answers)
    student: Student = get_student_info_from_lea(dirs[-1], due_date)
    grading.days_late = student.days_late

    give_feedback(student, grading, files, path)
