from __future__ import annotations
from dataclasses import dataclass


class Grading:
    """Class that holds the various sections and deductions for each section"""

    def __init__(self, manual_input: bool = True):
        self._sections: dict[str, Section] = {}
        self.title = ""
        self.days_late = 0
        self.penalty_per_day = 0.10
        self.rubric = dict()
        self.manual_input = manual_input

    def add_section(self, name: str, max_grade: float, min_grade: float = 0) -> Section:
        """
        add a section to the grading scheme
        :param name: name of the section
        :param max_grade: the default grade if no deductions
        :param min_grade: the minimum grade for this section
        """
        if name in self._sections:
            return self._sections[name]
        section = Section(name, max_grade, min_grade, self.manual_input)
        self._sections[section.name] = section
        return section

    @property
    def sections(self):
        return self._sections.values()

    def grade(self) -> float:
        """
        What is the final grade?
        """
        total = 0
        for section in self.sections:
            total += section.grade() * section.weight
        return total

    def out_of(self) -> int:
        """
        What is the maximum grade that could be obtained?
        """
        total = 0
        for section in self.sections:
            if "bonus" not in section.name:
                total += section.max_grade * section.weight
        return total

    def late_penalty(self) -> float:
        """
        Deduction based on late days
        """
        out_of = self.out_of()
        return self.days_late * self.penalty_per_day * out_of

    def __str__(self):
        return "\n".join(str(section) for section in self.sections)

    def serialize(self):
        """
        Return a string that summarizes this object
        """
        return str(self)

    @classmethod
    def de_serialize(cls, filename):
        """
        Read an appropriate string (from `serialize` function) and create
        a `group` object
        :param filename: the name of the file that contains the required info
        """
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
                    section_name, float(section_max), float(section_min)
                )

                if deduction is not None:
                    deduction_amt, deduction_descr = deduction.split(":", maxsplit=1)
                    section.add_result(deduction_descr, float(deduction_amt))
        return grade


class Section:
    """
    Creates a section within the rubric
    :param name: name of the section
    :param max_grade: the default grade if no deductions
    :param min_grade: the minimum grade for this section
    """

    separator = "|"

    def __init__(
        self,
        name: str,
        max_grade: float,
        min_grade: float = 0,
        manual_input: bool = True,
    ):
        self.deductions: list[Deductions] = []
        self.name = name.replace(Section.separator, " ")
        self.max_grade = max_grade
        self.min_grade = min_grade
        self.weight = 1
        self.manual_input = manual_input

    def ask_question(self, question, response, grade: float) -> str:
        """
        ask the teacher to answer a question
        :param question:
        :param response: this will be the response to the student if the answer to the question is no
        :param grade: the grade to be deducted if the answer is no to the question
        """
        ans = input(question + " ")
        if ans.strip() != "y":
            self.deductions.append(Deductions(grade, response))
        return ans

    def ask_question_with_feedback(self, question, grade: float) -> str:
        """
        ask the teacher to answer a question
        :param question:
        :param grade: the grade to be deducted if the answer is no to the question
        """
        ans = input(question + " ")
        if ans.strip() != "y":
            response = input("Give feedback: ")
            response = response.replace("\n", "<br>")
            self.deductions.append(Deductions(grade, question + ": " + response))
        return ans

    def ask_question_with_variable_grade(self, question) -> str:
        """
        ask the teacher to answer a question
        :param question:
        """
        ans = input(question + " ")
        if ans.strip() != "y":
            response = input("Give feedback: ")
            response = response.replace("\n", "<br>")
            grade = int(input("Deduction? "))
            self.deductions.append(Deductions(grade, question + ": " + response))
        return ans

    def ask_question_with_partial_grade(
        self, question: str, grade: float, ans: int = -1, response_ans: str = ""
    ):
        """
        ask the teacher to choose a 5-point scale grade for a question
        :param question:
        :param grade: the maximum score for the question
        :param ans: the 0-5 point "answer" for the partial grade (default -1, outside of range of possible values)
        :param response_ans: the 5-point scale text explanation
        """
        result, response = self._determine_partial_grade(
            question=question, grade=grade, ans=ans, response_ans=response_ans
        )
        deduction = abs(result - grade)
        self.deductions.append(Deductions(deduction, response))

    def add_result(self, response, grade: float):
        """
        add a response to the grading rubric
        :param response: what info will be given to the student
        :param grade: the value of the deduction
        """
        response = response.replace("\n", "<br>")
        self.deductions.append(Deductions(grade, response))

    def add_result_with_partial_grade(
        self, question, score, max_score, output, ans=-1, response_ans=""
    ):
        """
        add a grade to the grading rubric, with possibility for part marks (useful for unit tests)
        :param question:
        :param score: the score achieved on the unit test
        :param max_score: the maximum score for the question
        :param output: any message already available about the result (usually from unit test)
        :param ans: the 0-5 point "answer" for the partial grade (default -1, outside of range of possible values)
        :param response_ans: the 5-point scale text explanation
        """
        if score != max_score:
            result, response = self._determine_partial_grade(
                question.replace(":", ""),
                max_score,
                output=output,
                ans=ans,
                response_ans=response_ans,
            )
        else:
            result, response = score, f"{output.replace(':', '')}"
        deduction = abs(result - max_score)
        self.deductions.append(Deductions(deduction, response))

    def grade(self) -> float:
        """
        returns the final grade - but without late penalties
        """
        total = 0
        for evaluation in self.deductions:
            total += evaluation.deduction
        return min(max(self.min_grade, self.max_grade - total), self.max_grade)

    def clear_deductions(self):
        """
        Oops, we messed up, lets start over
        """
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

    def _determine_partial_grade(
        self, question, grade, output="", ans=-1, response_ans=""
    ) -> tuple(float, str):
        while ans < 0 or ans > 5:
            ans = (
                input(
                    f"\n{question}\n\t{output}\n\tAssign grade on 5 point scale (5 is perfect, 0 is not at all, etc): "
                )
                if self.manual_input
                else 0
            )
            try:
                ans = int(ans)
            except ValueError:
                ans = -1
        additional_feedback = (
            input("\tany additional feedback? Leave empty (hit enter) if no: ")
            if self.manual_input
            else ""
        )
        response_dict = {
            0: "incorrect",
            1: "attempted but significant issues",
            2: "attempted with major issues",
            3: "reasonable attempt with some issues",
            4: "good, with 1 or more small mistakes",
            5: "no issues",
        }
        result = (ans / 5) * grade
        if response_ans == "":
            response = f"{question}: {response_dict[ans]}. {additional_feedback}"
        else:
            response = f"{question}: {response_ans}. {additional_feedback}"
        return result, response


@dataclass
class Deductions:
    deduction: float
    feedback: str

    def __str__(self):
        return f"{self.deduction}: {self.feedback}"
