from jac_cs_grading_tools.grading import Grading
from jac_cs_grading_tools.unit_test import UnitTest
from jac_cs_grading_tools.rubric import Rubric


def run_tests(this_rubric: Rubric, results: dict[str, UnitTest]) -> Grading:
    grading = Grading()

    for section_info in this_rubric:
        skips = []
        print("\n\n", section_info.name)
        section = grading.add_section(
            section_info.name, section_info.worth, section_info.min_worth
        )
        for deduction in section_info.contents:
            # skip these tests if a prior test failed, and told us to skip
            if deduction.id in skips:
                continue

            # if there are automated tests for this, use result:
            if len(deduction.tests):
                msgs = []
                for test in deduction.tests:
                    if results[test].failed:
                        msgs.append(results[test].message)
                if len(msgs):
                    section.add_result(
                        deduction.feedback + "\n" + "\n".join(msgs), deduction.amount
                    )
                    skips = skips + deduction.skip_tests

            # if there are NO automated tests:
            else:
                if deduction.amount == 0:
                    section.ask_question_with_variable_grade(
                        f"Skip Deduction? {deduction.feedback}"
                    )
                elif deduction.feedback.endswith("MESSAGE"):
                    section.ask_question_with_feedback(
                        f"Skip Deduction? {deduction.amount} {deduction.feedback}",
                        deduction.amount,
                    )
                else:
                    section.ask_question(
                        f"Skip Deduction? {deduction.amount} {deduction.feedback}",
                        deduction.feedback,
                        deduction.amount,
                    )
    return grading
