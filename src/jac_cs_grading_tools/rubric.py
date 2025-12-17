from __future__ import annotations
import csv
from dataclasses import dataclass, field

SECTION = 0
SECTION_WORTH = 1
MINIMUM_POINTS = 2
DEDUCTION_ID = 3
DEDUCTION_AMT = 4
DEDUCTION_FEEDBACK = 5
DEDUCTION_TESTS = 6
SKIP = 7


class RubricError(Exception): pass


@dataclass
class RubricDeduction:
    id: str
    amount: float
    feedback: str
    tests: list[str] = field(default_factory=list)
    skip_tests: list[str] = field(default_factory=list)


@dataclass
class RubricSection:
    name: str
    worth: float
    min_worth: float = 0.0
    contents: list[RubricDeduction] = field(default_factory=list)


class Rubric:

    def __init__(self):
        self.sections: list[RubricSection] = []

    def __iter__(self):
        return iter(self.sections)

    def read_from_csv(self, filename: str) -> Rubric:
        with open(filename, "r", encoding='utf-8') as fh:
            # read the header line
            fh.readline()

            csv_fh = csv.reader(map(str.rstrip, fh))
            section = None
            for line in csv_fh:
                if len(line) < 1:
                    continue

                if line[SECTION] != "":
                    section = RubricSection(line[SECTION], float(line[SECTION_WORTH]), float(line[MINIMUM_POINTS]))
                    self.sections.append(section)

                elif line[DEDUCTION_ID] != "":
                    if section is None:
                        raise RubricError("Your rubric has a deduction which is not part of a section")
                    tests = []
                    if len(line) > DEDUCTION_TESTS:
                        tests = line[DEDUCTION_TESTS].split()
                    skip = []
                    if len(line) > SKIP:
                        skip = line[SKIP].split()
                    deduction = RubricDeduction(line[DEDUCTION_ID], float(line[DEDUCTION_AMT]),
                                                line[DEDUCTION_FEEDBACK], tests, skip)
                    section.contents.append(deduction)
        return self
