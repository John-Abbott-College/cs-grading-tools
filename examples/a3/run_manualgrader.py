from jac_cs_grading_tools.grading import Grading
import os
import sys
import json

grading = Grading()


def run_manual_tests(autograding_answers):
    section_docstrings = grading.add_section("Docstrings", 1)
    section_edits_required = grading.add_section("Submission issues", 1)
    section_coding_quality = grading.add_section("Code quality", 1)
    section_well_tested = grading.add_section("assignment3.py file used correctly", 1)

    # Docstrings filled in
    section_docstrings.ask_question_with_partial_grade(
        "docstring file descriptions are completed on each file", 1
    )

    # Edits required
    section_edits_required.ask_question_with_partial_grade(
        "no major edits required to get the code to work properly", 1
    )

    # Coding quality
    section_coding_quality.ask_question_with_partial_grade(
        "variables used appropriately", 1
    )

    # assignment3.py
    section_well_tested.ask_question_with_partial_grade(
        "assignment3.py used to test the my_functions.py functions", 1
    )

    # Put autograded results in Grading object
    with open(autograding_answers, mode="r") as f:
        autograder_results = json.load(f)

    for test in autograder_results["tests"]:
        test_section = grading.add_section(test["name"], 1)
        test_section.add_result_with_partial_grade(
            test.get("name"), test["score"], test["max_score"], test.get("output", "")
        )


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
