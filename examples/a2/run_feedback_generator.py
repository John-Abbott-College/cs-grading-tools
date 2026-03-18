import math
from datetime import datetime

from jac_cs_grading_tools.grading import Grading, Section
from jac_cs_grading_tools.feedback_utils import (
    get_student_info_from_lea,
    give_feedback,
    Student,
)
from jac_cs_grading_tools.check_util import errors_and_warnings
import os
import re
import sys

files = ["turtle-projectile.py"]
due_date = datetime(2025, 10, 22, 1)

# ===============================================================================
# ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("student submission directory AND rubric flag needed. Exiting.")
        sys.exit(1)
    path = sys.argv[1]
    rubric_generator = bool(int(sys.argv[2]))

    pathname = os.path.abspath(path)
    dirs = pathname.split(os.sep)

    manual_grading_answers = f"{path}test_answers.txt"

    if not os.path.exists(manual_grading_answers):
        print(
            "This student hasn't been graded yet -- no feedback or rubric can be generated"
        )
        sys.exit()

    grading = Grading.de_serialize(manual_grading_answers)
    student: Student = get_student_info_from_lea(dirs[-1], due_date)
    grading.days_late = student.days_late

    give_feedback(student, grading, files, path)
