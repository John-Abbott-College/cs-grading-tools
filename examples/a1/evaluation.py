import math
from datetime import datetime

from grading import Grading, Section
from feedback_utils import get_student_info_from_lea, give_feedback, Student
from check_util import run_top_level_code_return_output
import os
import re


def print_student_output(outputs):
    print()
    print("Student Output:")
    for output in map(str.rstrip, outputs):
        print("> ", output)
    print()


def qw(s: str) -> list[str]:
    return s.split(" ")


files = qw(
    "question_1_fix_me.py question_2_formatting.py question_3_toy_packing_plant.py "
    "question_4_tariffs.py question_5_recipe.py"
)

grading = Grading()


# ===============================================================================
# Coding quality
# ===============================================================================
def coding_quality():
    print("Coding Quality")
    print()
    section = grading.add_section("Part 0 - Coding Quality", 0, -5)
    print("Review the code")
    section.ask_question_with_feedback("Proper variable names (half deduction)?", 3)
    section.ask_question_with_feedback("Proper variable names?", 5)
    section.ask_question_with_feedback("No hard coding?", 3)


# ===============================================================================
# part I
# ===============================================================================
def fix_me():
    section = grading.add_section("Part I - fix me", 5)
    print("QUESTION 1 FIX ME")
    print()
    print(f"Running question 1 _fix_me.py using {files[0]=}")
    outputs = run_top_level_code_return_output(files[0])
    print_student_output(outputs)

    # part 1
    section.ask_question(
        "Did they print 9? (y/n)", "You did not add the two numbers", 1
    )
    # part 2
    section.ask_question(
        "Did they print 11? (y/n)", "You did not add the two numbers", 1
    )
    # part 3
    section.ask_question(
        "Did it run without crashing? (y/n)",
        "Your program is still crashing for part 3",
        2,
    )
    # part 4
    section.ask_question(
        "Was the square root of 2 printed (y/n)",
        "You did not print correct value for the square root of 2",
        1,
    )
    # part 5
    section.ask_question(
        "Was the pi printed to two decimal places (y/n)",
        "pi was not written to two decimal points",
        1,
    )

    section.ask_question_with_feedback_and_custom_grade(
        "Met requirements without needing code change?"
    )


# ===============================================================================
# part II
# ===============================================================================
def line_up_numbers():
    print("QUESTION 2 line up numbers")
    print()

    section = grading.add_section("Part II - line up numbers", 5)
    ans2, comment, outputs = decimal_point_line_up(files[1])
    print_student_output(outputs)

    if not ans2:
        feedback = "\nYour output:\n"
        for output in map(str.rstrip, outputs):
            feedback += f"`{output}`\n"
        section.add_result(feedback, 5)
    else:
        print("passed lining up numbers")

    for output in outputs:
        try:
            float(output)
        except ValueError:
            section.add_result(f"`{output}` is not a number :(", 2)
            break

    section.ask_question_with_feedback_and_custom_grade(
        "Met requirements without needing code change?"
    )


def decimal_point_line_up(filename):
    output = run_top_level_code_return_output(filename)
    pos = output[0].find(".")
    for line in output:
        if line.find(".") != pos:
            return (
                False,
                f"The decimals in your output do not line up. <br>Output: {output}<br>",
                output,
            )
    return True, "", output


# ===============================================================================
# part III
# ===============================================================================
def packing_up():
    print("QUESTION 3 packing up")
    print()
    section = grading.add_section("Part III - packing up", 15)

    # with original inputs
    did_pass = False
    outputs = run_top_level_code_return_output(files[2])
    print_student_output(outputs)

    if len(outputs) == 0:
        section.ask_question("Is there output?", "You need to print your answer!", 5)

    match = re.search(r"^.*?(\d+)\s*(\s+.*)$", outputs[-1])
    number = None
    if match:
        number = int(match.group(1))
    else:
        print("NO OUTPUT WAS FOUND... fix student code before continuing")
        input("Press enter to continue ")

    if number is not None and number == 31:
        print("passed")
        did_pass = True

    elif number is not None and number == 5:
        section.add_result(
            "You did not add the boxes that I boxed up during my shift", 10
        )

    elif number is not None and number <= 26:
        section.add_result("You forgot to add the initial number of full boxes", 5)

    elif number is not None and number == 29:
        section.add_result("You're calculation is off, the answer should be 31", 5)

    elif number is not None and number == 30:
        section.add_result(
            "You did not account for the toys that were in a partially filled box", 7
        )

    else:
        section.add_result("Your calculation is not correct", 15)

    # specific inputs, no extra filled box
    if did_pass:
        print()
        print("Running with toys to pack is 10")
        outputs = run_top_level_code_return_output(
            files[2], lambda x: x.replace("337", "10")
        )
        print_student_output(outputs)

        match = re.search(r"^.*(\d+)", outputs[-1])
        number = None
        if match:
            number = int(match.group(1))

        if number == 6:
            print("passed")

        else:
            section.add_result(
                "You did not account for the toys that were in a partially filled box",
                10,
            )

    section.ask_question_with_feedback_and_custom_grade(
        "Met requirements without needing code change?"
    )


# ===============================================================================
# part IV
# ===============================================================================
def tariffs():
    print("QUESTION 4 tariffs")
    print()
    section = grading.add_section("Part IV - tariffs", 15)

    dozen_eggs = 4.0
    bread = 3.0
    orange_juice = 5.0

    # part I
    farmer_price = 3 * dozen_eggs + 4 * bread + 2 * orange_juice
    wholesaler_price = farmer_price * 1.15
    store_price_no_tariffs = wholesaler_price * 1.20

    farmer_price = 3 * dozen_eggs + 4 * bread + 2 * orange_juice
    wholesaler_price = (farmer_price * 1.25) * 1.15
    store_price_with_tariffs = wholesaler_price * 1.20

    outputs = run_top_level_code_return_output(files[3])
    print_student_output(outputs)

    section.ask_question(
        "Is there output?",
        "You need to print your answer, or give an indication what the numbers represent",
        5,
    )
    ans2 = section.ask_question(
        f"Is the price before tariffs {store_price_no_tariffs}?",
        f"The price before tariffs should be {store_price_no_tariffs:.2f}: your gave... ",
        5,
    )
    ans1 = section.ask_question(
        f"Is the price after tariffs {store_price_with_tariffs:.2f}?",
        f"The price before tariffs should be {store_price_with_tariffs:.2f}: your gave... ",
        5,
    )
    if ans1 == "y" and ans2 == "y":
        section.ask_question(
            f"Is the difference in price {store_price_with_tariffs - store_price_no_tariffs:.2f}?",
            f"The price after tariffs should be {store_price_with_tariffs - store_price_no_tariffs}: "
            "your gave... ",
            5,
        )

    store_price = 450
    wholesaler_price = store_price / 1.20
    farmer_price = wholesaler_price / 1.15
    wholesaler_price = farmer_price * 1.25 * 1.15
    store_price_after_tariff = wholesaler_price * 1.20

    section.ask_question(
        f"Is the increase of grocery price {store_price_after_tariff - store_price:.2f}?",
        f"The increase of grocery prices should be {store_price_after_tariff - store_price:.2f}: "
        "you need to figure out the original farmer's price before recalculating your grocery bill.",
        3,
    )

    section.ask_question_with_feedback_and_custom_grade(
        "Met requirements without needing code change?"
    )


# ===============================================================================
# Section V
# ===============================================================================
def recipe():
    print("QUESTION 5 recipe")
    print()
    section = grading.add_section("Part V - recipe", 15)

    # given values
    number_of_cakes_to_bake = 150
    flour_container = 25 * 1000
    flour_per_cake = 355

    # adapt for whether they used input() or not
    is_using_var = section.ask_question(
        f"Check the student code: do they use a variable? (n if they use input())",
        f"Using input gives a small bonus grade.",
        -2,
    )

    # did they print the word flour??
    flour = False
    outputs = run_top_level_code_return_output(files[4], inputs=["150"])
    print_student_output(outputs)

    for line in map(str.rstrip, outputs):
        flour = flour or "flour" in line.lower()
    if not flour:
        section.add_result("You did not print how much flour was needed!", 5)
        print("Did not print how much flour was needed")

    # answer this question just in case you had to fix their code to get the other stuff
    # to work
    section.ask_question(
        "Did they print the word 'flour'",
        "Writing numbers without descriptions is not a useful "
        "program, because how do I know what I need to buy at the grocery store?",
        5,
    )

    # the correct answer for 150 cakes
    passed = True
    answer = math.ceil(number_of_cakes_to_bake * flour_per_cake / flour_container)
    for output in map(str.strip, outputs):
        if "flour" in output.lower():
            match = re.search(rf"(^|.*\s){answer}(\s|$)", output)
            if not match:
                passed = False
            else:
                print("Passed for 150 cakes")
            break
    if not passed:
        answer = int(number_of_cakes_to_bake * flour_per_cake / flour_container)
        for output in map(str.strip, outputs):
            partial_pass = False
            if "flour" in output.lower():
                match = re.search(rf"(^|.*\s){answer}(\s|$)", output)
                if match:
                    print("You did NOT round up")
                    section.add_result(
                        "You have to round up or you will not have enough ingredients",
                        10,
                    )
                    partial_pass = True
                match = re.search(rf"(^|.*\s)(\d+\..*)(\s|$)", output)
                if match:
                    print("You cannot buy partial bags of flour!")
                    section.add_result(
                        f"You cannot buy partial bags of flour {match.group(2)}", 10
                    )
                    partial_pass = True
                if not partial_pass:
                    section.add_result(
                        f"Your answer for number of bags of flour is incorrect", 15
                    )

    if passed:
        number_of_cakes_to_bake = 5000
        outputs = run_top_level_code_return_output(
            files[4],
            lambda x: x.replace(
                "number_of_cakes_to_bake = 150", "number_of_cakes_to_bake = 5000"
            ),
            inputs=["5000"],
        )
        print(
            "Exact number of bags needs to be purchased: bake 500 cakes, 71 bags flour needed"
        )
        print_student_output(outputs)
        answer = math.ceil(number_of_cakes_to_bake * flour_per_cake / flour_container)
        for output in map(str.strip, outputs):
            if "flour" in output.lower():
                match = re.search(rf"(^|.*\s){answer}(\s|$)", output)
                if not match:
                    section.add_result(
                        "For 5000 cakes, you should need exactly 71 "
                        f"bags, but instead you have '{output}'",
                        5,
                    )
                    print("Failed for 5000 cakes")
                else:
                    print("Passed for 5000 cakes")
                break

        number_of_cakes_to_bake = 2
        outputs = run_top_level_code_return_output(
            files[4],
            lambda x: x.replace(
                "number_of_cakes_to_bake = 150", "number_of_cakes_to_bake = 2"
            ),
            inputs=["2"],
        )
        print("Small number of cakes to bake: bake 2 cakes, 1 bags flour needed")
        print_student_output(outputs)
        answer = math.ceil(number_of_cakes_to_bake * flour_per_cake / flour_container)
        for output in map(str.strip, outputs):
            if "flour" in output.lower():
                match = re.search(rf"(^|.*\s){answer}(\s|$)", output)
                if not match:
                    section.add_result(
                        "For 2 cakes, you should need 1 "
                        f"bag, but instead you have '{output}'",
                        5,
                    )
                    print("Failed for 2 cakes")
                else:
                    print("Passed for 2 cakes")
                break

    section.ask_question_with_feedback_and_custom_grade(
        "Met requirements without needing code change?"
    )


# ===============================================================================
# ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    due_date = datetime(2025, 9, 24, 1)

    pathname = os.path.abspath(".")
    dirs = pathname.split(os.sep)
    student: Student = get_student_info_from_lea(dirs[-1], due_date)

    print(f"{student}")
    print("WE ARE ASSUMING YOU ARE RUNNING FROM THE STUDENT'S DIRECTORY")

    grading = Grading()
    grading.days_late = student.days_late

    while True:
        fix_me()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    while True:
        line_up_numbers()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    while True:
        packing_up()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    while True:
        tariffs()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    while True:
        recipe()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    while True:
        coding_quality()
        ans = input("Continue to next session? (y/n) ")
        if ans.rstrip() == "y":
            break

    give_feedback(student, grading, files)
