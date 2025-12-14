import math
from datetime import datetime

from grading import Grading, Section
from feedback_utils import get_student_info_from_lea, give_feedback, Student
from check_util import run_top_level_code_return_output, errors_and_warnings
import os
import re
import sys

files = ["my_functions.py", "assignment3.py"]

# ===============================================================================
# if test_answers.txt is not found, then ask the questions
# ===============================================================================
manual_test_results = dict()

grading = Grading()


def run_manual_tests():
    section_coding_quality = grading.add_section("Coding Quality", 0, -1)
    section_edits_required = grading.add_section("Edits required", -1)

    # Coding quality
    all_errors, all_warnings = errors_and_warnings(files)
    section_coding_quality.add_result(f"Warnings:\n{all_warnings}", 0)
    section_coding_quality.ask_question_with_feedback("Are the variables good?", 1)
    section_coding_quality.ask_question(
        "Did you use variable names instead of numbers?",
        "Use the variables given, not the actual numbers (using numbers makes it harder to read what your code is doing, "
        "and is more prone to mistakes)",
        1,
    )
    section_coding_quality.ask_question_with_feedback("No dead (unused) code?", 1)

    # Edits required
    section_edits_required.ask_question_with_feedback(
        "Were major edits required to get the code to work properly?"
        "Major edits were required to get the code to work properly.",
        1,
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
    if not os.path.exists(manual_grading_answers):
        run_manual_tests()
        with open(manual_grading_answers, "w", encoding="utf-8") as fh:
            print(str(grading), file=fh)

    else:
        ans = input("Do you want to re-answer questions? ")
        if "y" in ans:
            run_manual_tests()
            with open(manual_grading_answers, "w", encoding="utf-8") as fh:
                print(str(grading), file=fh)

    grading = Grading.de_serialize(manual_grading_answers)
    student: Student = get_student_info_from_lea(dirs[-1], due_date)
    grading.days_late = student.days_late

    give_feedback(student, grading, files, path)
