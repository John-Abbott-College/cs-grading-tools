from __future__ import annotations
from dataclasses import dataclass
from typing import Generator


class Grading:
    def __init__(self):
        self._sections: dict[Section] = {}
        self.title = ""
        self.days_late = 0
        self.penalty_per_day = 0.10
        self.rubric = dict()

    def add_section(self, name, max_grade, min_grade=0) -> Section:
        if name in self._sections:
            return self._sections[name]
        section = Section(name, max_grade, min_grade)
        self._sections[section.name] = section
        return section

    @property
    def sections(self):
        return self._sections.values()

    def grade(self) -> float:
        out_of = 0
        total = 0
        for section in self.sections:
            out_of += section.max_grade * section.weight
            total += section.grade() * section.weight
        return total

    def out_of(self) -> int:
        total = 0
        for section in self.sections:
            total += section.max_grade * section.weight
        return total

    def late_penalty(self) -> float:
        out_of = self.out_of()
        return self.days_late * self.penalty_per_day * out_of

    def __str__(self):
        return "\n".join(str(section) for section in self.sections)

    def serialize(self):
        return str(self)

    @classmethod
    def de_serialize(cls, filename):
        grade = cls()
        with open(filename, "r", encoding="utf-8") as fh:
            for line in map(str.rstrip, fh):
                if line == "":
                    continue

                deduction = None
                section = line
                if ":" in line:
                    section, deduction = line.split(":", maxsplit=1)

                section_name, section_max, section_min = section.split(
                    Section.separator
                )
                section = grade.add_section(
                    section_name, int(section_max), int(section_min)
                )

                if deduction is not None:
                    deduction_amt, deduction_descr = deduction.split(":", maxsplit=1)
                    section.add_result(deduction_descr, float(deduction_amt))
        return grade


class Section:
    separator = "|"

    def __init__(self, name, max_grade: int, min_grade: int = 0):
        self.deductions: list[Deductions] = []
        self.name = name.replace(Section.separator, " ")
        self.max_grade = max_grade
        self.min_grade = min_grade
        self.weight = 1

    def ask_question(self, question, response, grade: float) -> str:
        ans = input(question + " ")
        if ans.strip() != "y":
            self.deductions.append(Deductions(grade, response))
        return ans

    def ask_question_with_feedback(self, question, grade: float) -> str:
        ans = input(question + " ")
        if ans.strip() != "y":
            response = input("Give feedback: ")
            response = response.replace("\n", "<br>")
            self.deductions.append(Deductions(grade, question + ": " + response))
        return ans

    def ask_question_with_partial_grade(self, question, grade: float):
        result, response = self._determine_partial_grade(question=question, grade=grade)
        deduction = abs(result - grade)
        self.deductions.append(Deductions(deduction, response))


    def add_result(self, response, grade: float):
        response = response.replace("\n", "<br>")
        self.deductions.append(Deductions(grade, response))
        print(response)

    def add_result_with_partial_grade(self, question, score, max_score):
        if score != max_score:
            result, response = self._determine_partial_grade(question.replace(":",""), max_score)
        else:
            result, response = score, f"{question.replace(":","")}"
        deduction = abs(result - max_score)
        self.deductions.append(Deductions(deduction, response))

    def grade(self) -> float:
        total = 0
        for evaluation in self.deductions:
            total += evaluation.deduction
        return min(max(self.min_grade, self.max_grade - total), self.max_grade)

    def clear_deductions(self):
        self.deductions.clear()

    def __str__(self):
        section_info = Section.separator.join(
            (self.name, str(self.max_grade), str(self.min_grade))
        )
        return (
            section_info
            + "\n"
            + "\n".join(f"{section_info}:{str(d)}" for d in self.deductions)
        )

    def _determine_partial_grade(self, question, grade) -> tuple(float, str):
        ans = -1
        while ans < 0 or ans > 5:
            ans = input(f"{question} Assign grade on 5 point scale (5 is perfect, 0 is not at all, etc) ")
            try:
                ans = int(ans)
            except ValueError:
                pass
        additional_feedback = input(f"any additional feedback? Leave empty (hit enter) if no ")
        response_dict = {
            0: "not done",
            1: "attempted but significant issues",
            2: "attempted with major issues",
            3: "reasonable attempt with some issues",
            4: "good, with 1 or more small mistakes",
            5: "perfect"
        }
        result = (ans / 5) * grade
        response = f"{question}: {response_dict[ans]}. {additional_feedback}"
        return result, response


@dataclass
class Deductions:
    deduction: float
    feedback: str

    def __str__(self):
        return f"{self.deduction}:{self.feedback}"
