from __future__ import annotations
from dataclasses import dataclass


class Grading:
    def __init__(self):
        self._sections: dict[Section] = {}
        self.title = ""
        self.days_late = 0
        self.penalty_per_day = 0.10

    def add_section(self, name, max_grade, min_grade=0) -> Section:
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
            out_of += section.max_grade
            total += section.grade()
        return total

    def out_of(self) -> int:
        total = 0
        for section in self.sections:
            total += section.max_grade
        return total

    def late_penalty(self) -> float:
        return self.days_late * self.penalty_per_day * self.out_of()


class Section:
    def __init__(self, name, max_grade: int, min_grade: int):
        self.deductions: list[Deductions] = []
        self.name = name
        self.max_grade = max_grade
        self.min_grade = min_grade
        self.weight = self.max_grade

    def ask_question(self, question, response, grade: float) -> str:
        ans = input(question + " ")
        if ans.strip() != "y":
            self.deductions.append(Deductions(grade, response))
        return ans

    def ask_question_with_feedback(self, question, grade: float) -> str:
        ans = input(question + " ")
        if ans.strip() != "y":
            response = input("Give feedback: ")
            self.deductions.append(Deductions(grade, question + ": " + response))
        return ans


    def ask_question_with_feedback_and_custom_grade(self, question) -> str:
        ans = input(question + " ")
        if ans.strip() != "y":
            response = input("Give feedback: ")
            grade = float(input("Points to deduct: "))
            self.deductions.append(Deductions(grade, question + ": " + response))
        return ans

    def add_result(self, response, grade: float):
        self.deductions.append(Deductions(grade, response))
        print(response)

    def grade(self) -> float:
        total = 0
        for evaluation in self.deductions:
            total += evaluation.deduction
        # return min(max(self.min_grade, self.max_grade - total), self.max_grade)
        return max(self.min_grade, self.max_grade - total)

    def clear_deductions(self):
        self.deductions.clear()



@dataclass
class Deductions:
    deduction: float
    feedback: str
