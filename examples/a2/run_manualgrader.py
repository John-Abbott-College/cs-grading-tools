from datetime import datetime

from jac_cs_grading_tools.grading import Grading
from jac_cs_grading_tools.feedback_utils import (
    get_student_info_from_lea,
    give_feedback,
    Student,
)
from jac_cs_grading_tools.check_util import errors_and_warnings
import os
import sys

files = ["turtle-projectile.py"]

grading = Grading()

def run_manual_tests():
    print("EDIT THE STUDENT ASSIGNMENT AND REMOVE WIND!!!")

    print("Before beginning, start the student's turtle assignment")
    print("RUN THIS PROGRAM FROM THE STUDENT DIRECTORY!!")

    section_coding_quality = grading.add_section("Coding Quality", 0, -10)
    section_background = grading.add_section("I. Draw the Background", 20)
    section_initialization = grading.add_section("II. Initialization", 10)
    section_basic_motion = grading.add_section("III. Basic Motion", 35)
    section_hit_ground = grading.add_section(
        "IV. Stopping the Turtle when it hits the ground or the ocean", 20
    )
    section_hit_wall = grading.add_section(
        "V. Stopping the Turtle if it hits the wall", 10
    )
    section_wind = grading.add_section("VI. Wind", 5)

    # Coding quality
    section_coding_quality.ask_question_with_partial_grade("Are the variables good?", 5)
    section_coding_quality.ask_question_with_partial_grade(
        "Did you use variable names instead of numbers?", 5
    )
    section_coding_quality.ask_question_with_partial_grade("No dead code?", 5)

    # background
    section_background.ask_question_with_partial_grade(
        "Were the ground and pond rectangles drawn", 15
    )

    section_background.ask_question_with_partial_grade(
        "Were the ground and pond rectangles drawn in the correct spot", 10
    )

    section_background.ask_question_with_partial_grade("Was the wall drawn", 10)

    # initialization
    print()
    print("Use angle: 70, speed: 90")

    section_initialization.ask_question_with_partial_grade(
        "Did the program ask for angle and velocity",
        "You did not ask the user to enter the angle and/or the velocity",
        10,
    )

    section_initialization.ask_question_with_partial_grade(
        "Angle / Velocity question... was it a good prompt?", 10
    )

    # basic motion

    section_basic_motion.ask_question_with_partial_grade("Does the turtle move?", 35)

    section_basic_motion.ask_question_with_partial_grade(
        "Does the turtle movement look correct", 25
    )

    section_basic_motion.ask_question_with_partial_grade(
        "Did the turtle enter the ocean?", 15
    )

    section_basic_motion.ask_question_with_partial_grade(
        "Does the turtle always 'face' the right direction", 10
    )

    section_basic_motion.ask_question_with_partial_grade(
        "Does the turtle show its path?", 2
    )

    # hitting the ground/ocean
    print()
    print(
        "If the turtle didn't hit the ocean, play around till you get it to hit the ocean"
    )

    section_hit_ground.ask_question_with_partial_grade(
        "Using appropriate angle/speed, does the program detect that the turtle hit the ocean?",
        10,
    )

    section_hit_ground.ask_question_with_partial_grade(
        "Using angle 20, speed 20, does the program detect that the turtle hit the ground?",
        20,
    )

    section_hit_ground.ask_question_with_partial_grade(
        "Using angle 70, speed 100, does the program detect that the turtle hit the ground?",
        20,
    )

    # hitting the wall
    section_hit_wall.ask_question_with_partial_grade(
        "Using angle 20, speed 200, does program detect that the turtle hit a wall?",
        5,
    )
    section_hit_wall.ask_question_with_partial_grade(
        "Using angle 45, speed 70, does program detect that the turtle hit a wall?",
        10,
    )

    # wind
    print(
        "\nFor wind calculations, use 56 velocity, 45 degree angle, wind 40, direction 180"
    )
    section_wind.ask_question_with_partial_grade(
        "Was wind speed used and not acceleration?", 5
    )

    section_wind.ask_question_with_partial_grade(
        "If wind is 40, and angle is 180, and turtle is 45/56, does the turtle go up down?",
        5,
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
