import math
from datetime import datetime

from grading import Grading, Section
from feedback_utils import get_student_info_from_lea, give_feedback, Student
from check_util import run_top_level_code_return_output, errors_and_warnings
import os
import re

files = ["turtle_projectile.py"]

# ===============================================================================
# if test_answers.txt is not found, then ask the questions
# ===============================================================================
manual_test_results = dict()

grading = Grading()


def run_manual_tests():
    print("EDIT THE STUDENT ASSIGNMENT AND REMOVE WIND!!!")

    print("Before beginning, start the student's turtle assignment")
    print("RUN THIS PROGRAM FROM THE STUDENT DIRECTORY!!")

    section_coding_quality = grading.add_section("Coding Quality", 0, -10)
    section_background = grading.add_section("I. Draw the Background", 20)
    section_initialization = grading.add_section("II. Initialization", 10)
    section_basic_motion = grading.add_section("III. Basic Motion", 35)
    section_hit_ground = grading.add_section("IV. Stopping the Turtle when it hits the ground or the ocean", 20)
    section_hit_wall = grading.add_section("V. Stopping the Turtle if it hits the wall", 10)
    section_wind = grading.add_section("VI. Wind", 5)

    # Coding quality
    all_errors, all_warnings = errors_and_warnings(files)
    section_coding_quality.add_result(f"Warnings:\n{all_warnings}", 0)
    section_coding_quality.ask_question_with_feedback("Are the variables good?", 5)
    section_coding_quality.ask_question(
        "Did you use variable names instead of numbers?",
        "Use the variables given, not the actual numbers (using numbers makes it harder to read what your code is doing, "
        "and is more prone to mistakes)", 5)
    section_coding_quality.ask_question_with_feedback("No dead code?", 5)

    # background
    section_background.ask_question(
        "Were the ground and pond rectangles drawn",
        "Ground and Ocean rectangles were not drawn", 15)

    section_background.ask_question(
        "Were the ground and pond rectangles drawn in the correct spot",
        "Ocean and ground rectangles were not drawn in the correct spots", 10)

    section_background.ask_question(
        "Was the wall drawn drawn",
        "Wall was not drawn correctly", 10)

    # initialization
    print()
    print("Use angle: 70, speed: 90")

    section_initialization.ask_question(
        "Did the program ask for angle and velocity",
        "You did not ask the user to enter the angle and/or the velocity", 10)

    section_initialization.ask_question_with_feedback(
        "Angle / Velocity question... was it a good prompt?", 10)

    # basic motion

    section_basic_motion.ask_question(
        "Does the turtle move?",
        "Your baby turtle doesn't move :(", 35)

    section_basic_motion.ask_question_with_feedback(
        "Is the turtle movement look correct", 25)

    section_basic_motion.ask_question(
        "Did the turtle enter the ocean?",
        "There is something wrong with your kinematic equations, "
        "You should hit the pond at angle 70 and speed 90", 15)

    section_basic_motion.ask_question(
        "Does the turtle always 'face' the right direction",
        "Your turtle does not always face the correct direction ", 10)

    section_basic_motion.ask_question(
        "Does the turtle show its path?",
        "Put the `pen` down while moving the turtle ", 2)

    # hitting the ground/ocean
    print()
    print("If the turtle didn't hit the ocean, play around till you get it to hit the ocean")

    section_hit_ground.ask_question(
        "Using appropriate angle/speed, does the program detect that the turtle hit the ocean?",
        "You did not detect that the turtle hit the ocean", 10)

    section_hit_ground.ask_question(
        "Using angle 20, speed 20, does the program detect that the turtle hit the ground?",
        "You did not detect that the turtle hit the ground before the wall", 20)

    section_hit_ground.ask_question(
        "Using angle 70, speed 100, does the program detect that the turtle hit the ground?",
        "You did not detect that the turtle hit the ground on the other side of the wall", 20)

    # hitting the wall
    section_hit_wall.ask_question(
        "Using angle 20, speed 200, does program detect that the turtle hit a wall?",
        "You did not detect if the turtle hit the wall at angle 20, speed 200", 5)
    section_hit_wall.ask_question(
        "Using angle 45, speed 70, does program detect that the turtle hit a wall?",
        "You did not detect if the turtle hit the wall at angle 45, speed 70", 10)

    # wind
    print("\nFor wind calculations, use 56 velocity, 45 degree angle, wind 40, direction 180")
    section_wind.ask_question(
        "Was wind speed used and not acceleration?",
        "If the turtle x velocity is exactly opposite the wind x velocity, "
        "your turtle should just go straight up and down.  It doesn't. "
        "You used wind acceleration instead of wind speed",5)

    section_wind.ask_question(
        "If wind is 40, and angle is 180, and turtle is 45/56, does the turtle go up down?",
        "If the turtle x velocity is exactly opposite the wind x velocity, "
        "your turtle should just go straight up and down.  It doesn't",5)


# ===============================================================================
# ENTRY POINT
# ===============================================================================

if __name__ == "__main__":
    due_date = datetime(2025, 3, 14, 8)

    print("WE ARE ASSUMING YOU ARE RUNNING FROM THE STUDENT'S DIRECTORY")
    pathname = os.path.abspath(".")
    dirs = pathname.split(os.sep)

    test_answer = "test_answers.txt"
    if not os.path.exists(test_answer):
        run_manual_tests()
        with open (test_answer,"w",encoding='utf-8') as fh:
            print(str(grading), file=fh)

    else:
        ans = input("Do you want to re-answer questions? ")
        if "y" in ans:
            run_manual_tests()
            with open (test_answer,"w",encoding='utf-8') as fh:
                print(str(grading), file=fh)

    grading = Grading.de_serialize(test_answer)
    student: Student = get_student_info_from_lea(dirs[-1], due_date)
    grading.days_late = student.days_late


    give_feedback(student, grading, files)
