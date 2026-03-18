import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, TextIO

from jac_cs_grading_tools.grading import Grading

OUTPUT_COMMENTS: list[tuple[range, str]] = [
    (range(100, 200), "Perfect!"),
    (range(90, 100), "Excellent!"),
    (range(80, 90), "Great!"),
    (range(70, 80), "Good!"),
    (range(60, 70), "Good."),
    (range(0, 60), "See me and we can go over this assignment."),
]


@dataclass
class Student:
    """Student object
    :param id:
    :param name:
    :param submission_date: datetime object
    :days_late: float
    """

    id: str
    name: str
    submission_date: datetime
    days_late: float


def get_student_info_from_lea(
    folder_name: str, due_date: Optional[datetime] = None
) -> Student:
    """
    parse student folder name from LEA to create
    :param due_date: date the assignment was due
    :param folder_name: name of the folder that LEA created when downloading assignment
    """
    basename = os.path.basename(folder_name)
    if match := re.match(r"(.*?)_(\d{7})_.*?Submitted_on_(.*)$", basename):
        student_id: str = match.groups()[1]
        student_name: str = match.groups()[0]
        submitted_str = match.groups()[2]
        try:
            submitted: datetime = datetime.strptime(submitted_str, "%Y-%m-%d_%Hh%Mm%Ss")
        except ValueError:
            submitted: datetime = datetime(2000, 1, 0, 1)
    else:
        raise TypeError("Folder name does not match the format from LEA")

    days_late = None
    if due_date is not None:
        late: timedelta = submitted - due_date
        days_late = late.days + late.seconds / (24 * 60 * 60)
        days_late = days_late if days_late > 0 else 0

    student = Student(
        id=student_id, name=student_name, submission_date=submitted, days_late=days_late
    )
    return student


# ----------------------------------------------------------------------------------------
def give_feedback(
    student: Student,
    evaluation: Grading,
    source_files: list[str] = None,
    file_prefix: str = "",
):
    student_prefix = f"{file_prefix}{student.id}_{student.name}"
    feedback_file = f"{student_prefix}.md"
    grading_csv = f"{student_prefix}.csv"

    with open(feedback_file, "w") as fh:
        print_evaluation(student, evaluation, fh, source_files)

    with open(grading_csv, "w") as fh:
        print_grades(student, evaluation, fh)


# =============================================================================
# print
# =============================================================================


def print_grades(student: Student, evaluation: Grading, file: TextIO = sys.stdout):
    final_grade = max(evaluation.grade() - evaluation.late_penalty(), 0)
    file.write(f"{student.name},{student.id},{final_grade},See LEA for feedback.")


def print_evaluation(
    student: Student, evaluation: Grading, file: TextIO = sys.stdout, source_files=None
):
    if source_files is None:
        source_files = []

    grade = evaluation.grade()
    formatter = MarkDownFormat()

    # print header
    pct = grade / evaluation.out_of() * 100
    comment = ""
    for r, comment in OUTPUT_COMMENTS:
        if int(pct) in r:
            break

    final_grade = max(evaluation.grade() - evaluation.late_penalty(), 0)

    file.write(formatter.header())
    file.write(
        formatter.title(
            title=evaluation.title, score=final_grade, max_grade=evaluation.out_of()
        )
    )
    file.write(
        formatter.student_info(student=student, evaluation=evaluation, comment=comment)
    )

    # print sections and deductions
    file.write(formatter.result_header())
    for section in evaluation.sections:
        file.write(
            formatter.section_header(
                name=section.name,
                score=section.grade() * section.weight,
                max_grade=section.max_grade * section.weight,
            )
        )
        for d in section.deductions:
            file.write(
                formatter.deduction(
                    feedback=d.feedback, deduction=d.deduction * section.weight
                )
            )

    # print student code
    file.write("\n")
    file.write(formatter.code_header())
    for code_file in source_files:
        if os.path.exists(code_file) and os.path.isfile(code_file):
            # print(f"opening file {code_file}")
            with open(code_file, "r") as fh:
                code_str = fh.read()
            filename = os.path.basename(code_file)
            file.write(formatter.code_file(filename, code_str))


# =============================================================================
# Markdown formatted template
# =============================================================================
class MarkDownFormat:
    @staticmethod
    def header():
        return ""

    @staticmethod
    def title(title: str, score: float, max_grade: int) -> str:
        return f"# {title} [{score}/{max_grade}]\n"

    @staticmethod
    def student_info(student: Student, evaluation: Grading, comment: str) -> str:
        final_grade = max(evaluation.grade() - evaluation.late_penalty(), 0)
        return f"""
|                 |                                                                                                   |
|-----------------|---------------------------------------------------------------------------------------------------|
| StudentID       | {student.id}                                                                                      |
| Name            | {student.name}                                                                                    |
| Submitted       | {student.submission_date}                                                                         |
| Late            | -{evaluation.late_penalty(): .2f}   ({student.days_late: .2f} days)                               |
| Grade           | {evaluation.grade():.2f} - {evaluation.late_penalty(): .2f}                                       |
| Final Grade     | {final_grade:.2f} out of {evaluation.out_of()} ({final_grade / evaluation.out_of() * 100: 3.2f}%) |

"""

    @staticmethod
    def section_header(name: str, score: float, max_grade: float) -> str:
        return f"* [`{score:6.2f}/{max_grade:3.2f}`] **{name}**\n"

    @staticmethod
    def deduction(feedback: str, deduction: float) -> str:
        return f"  * `[-{deduction:5.2f}]`  {feedback}  \n"

    @staticmethod
    def result_header() -> str:
        return "### Results:\n\n"

    @staticmethod
    def code_header() -> str:
        return "## Code\n"

    @staticmethod
    def code_file(filename: str, code: str) -> str:
        return f"""
### {filename}

```python
{code}
```

"""
