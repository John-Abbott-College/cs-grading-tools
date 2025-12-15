import os
import unittest
import math
from os.path import splitext
from gradescope_utils.autograder_utils.decorators import weight

from test_helper import (
    get_inner_func,
    uses_loop,
    get_signature,
    get_func_calls,
    contains_func,
    uses_condition,
)

files_to_test = {"func_file": "my_functions.py", "main_file": "assignment3.py"}

FLOAT_PRECISION_TOL = 2


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.files_to_test = list(files_to_test.values())

    @weight(1)
    def test_source_files(self):
        """Check submitted code files"""
        for file in self.files_to_test:
            self.assertTrue(os.path.isfile(file), f"Cannot find {file}")
        print("All source code were files submitted!")


class TestFuncSig(unittest.TestCase):
    def setUp(self):
        try:
            py_file, extension = splitext(files_to_test["func_file"])
            self.student_code = __import__(py_file)
            self.functions_to_check = [
                "net_income",
                "concentration_percent",
                "intake_frequency",
                "gcd",
                "hex_area",
                "green_area",
            ]
            self.expected_return_types = [float, float, int, int, float, float]
            self.expected_count_params = [2, 2, 1, 2, 1, 3]
        except ModuleNotFoundError as e:
            print(e)
            self.fail(f"Cannot find {files_to_test['func_file']}. Did you rename it?")
        except Exception as e:
            self.fail(f"Unknown error occurred {e}. Reach out to teacher.")

    @weight(1)
    def test_check_for_inner_functions(self):
        """Scanning functions indentation level"""
        function_dict = get_inner_func(self.student_code)
        for func, inner_list in function_dict.items():
            msg = ", ".join(i + "()" for i in inner_list)
            self.assertEqual(
                len(inner_list),
                0,
                f"Oops! It looks like you've defined the function(s) "
                f"{msg} inside the function {func}(). "
                f"Remember to define your functions at the same level of indentation to ensure they "
                f"can be accessible to other python scripts",
            )
        print(
            "Great, all your functions are defined at the correct level of indentation."
        )

    @weight(1)
    def test_function_definitions(self):
        """Checking if all the functions are there"""
        for func_name in self.functions_to_check:
            self.assertTrue(
                contains_func(self.student_code, func_name),
                f"This function {func_name} was not found "
                f"in {self.student_code.__name__}",
            )
        print("Good job! All required functions are present.")

    @weight(1)
    def test_function_signatures(self):
        """Checking all the functions' signatures"""
        try:
            for func_name, params_count in zip(
                self.functions_to_check,
                self.expected_count_params,
            ):
                sig = get_signature(self.student_code.__getattribute__(func_name))
                actual_param_count = len(sig.parameters)
                self.assertEqual(
                    params_count,
                    actual_param_count,
                    f"Oops, the function {func_name} should take {params_count} not {actual_param_count}",
                )
        except ModuleNotFoundError:
            self.fail(f"Couldn't find {self.student_code.__name__}")
        except AttributeError as a:
            self.fail(f"You forgot to submit this function {a}")
        except Exception as e:
            self.fail(f"Unknown error{e}")
        print("Good job! All functions have the correct number of parameters")


class TestQ1Evaluator(unittest.TestCase):
    def setUp(self):
        try:
            py_file, extension = splitext(files_to_test["func_file"])
            TAX_BRACKET_LOW = 53_255
            TAX_BRACKET_MED = 106_495
            TAX_BRACKET_HIGH = 129_590
            INCOME_ABOVE_HIGHEST = 150_000
            TAX_RATE_LOW = 0.14
            TAX_RATE_MED = 0.19
            TAX_RATE_HIGH = 0.24
            TAX_RATE_ULTRA = 0.2575
            self.income_brackets = [
                TAX_BRACKET_LOW,
                TAX_BRACKET_MED,
                TAX_BRACKET_HIGH,
                INCOME_ABOVE_HIGHEST,
            ]
            self.tax_rates = [TAX_RATE_LOW, TAX_RATE_MED, TAX_RATE_HIGH, TAX_RATE_ULTRA]
            self.weeks_per_year = 52
            self.file_to_test = py_file
            self.student_code = __import__(py_file)
        except ModuleNotFoundError:
            self.fail(f"No file named {self.file_to_test}. Di you rename it? ")
        except Exception as e:
            self.fail(f"Unknown error {e}")

    @weight(1)
    def test_accuracy(self):
        """Accuracy Test net_income()"""
        gross_income = (
            self.income_brackets[0] - 10
        )  # ensuring it's a value in the first bracket
        tax_rate = self.tax_rates[0]
        expected_net_income = gross_income * (1 - tax_rate)
        hours_per_week = 25
        total_hours = hours_per_week * self.weeks_per_year
        hourly_rate = gross_income / total_hours
        try:
            actual_net_income = self.student_code.net_income(
                hourly_rate=hourly_rate, hours_per_week=hours_per_week
            )
            self.assertAlmostEqual(
                expected_net_income,
                actual_net_income,
                places=FLOAT_PRECISION_TOL,
                msg=f"Mistake in the income calculation, for hourly_salary={hourly_rate}, "
                f"hours_per_week={hours_per_week}. Expected net income {expected_net_income:.2f}$"
                f"But got: {actual_net_income:.2f}$",
            )
        except Exception as e:
            self.fail(e)
        print("Perfect! Correctly calculated!")

    @weight(1)
    def test_conditionals(self):
        """Logic Test net_income()"""
        try:
            weekly_hours = 40
            total_hours = weekly_hours * self.weeks_per_year
            for gross_income, tax_rate in zip(self.income_brackets, self.tax_rates):
                expected_income = (gross_income - 10) * (1 - tax_rate)
                calculated_income = self.student_code.net_income(
                    hourly_rate=gross_income / total_hours, hours_per_week=weekly_hours
                )
                self.assertAlmostEqual(
                    expected_income,
                    calculated_income,
                    places=6,
                    msg=f"For a gross salary of {gross_income:.2f}$, I expect a net salary of {expected_income:.2f}$, but got {calculated_income:.2f}$",
                )

        except Exception as e:
            self.fail(e)
        print("Perfect! Correctly calculated!")


class TestQ2Evaluator(unittest.TestCase):
    def setUp(self):
        try:
            py_file, extension = splitext(files_to_test["func_file"])
            self.file_to_test = py_file
            self.student_code = __import__(py_file)
        except ModuleNotFoundError:
            self.fail(f"No file named {files_to_test}.")
        except Exception as e:
            self.fail(f"Unknown error {e}")

    @weight(1)
    def test_concentration_accuracy(self):
        """Accuracy Test concentration_percent()"""
        try:
            expected = 1  # or 100%
            value = self.student_code.concentration_percent(half_life=5, time=0)
            tol = 10 ** (-FLOAT_PRECISION_TOL)
            is_equal = math.isclose(expected, value, abs_tol=tol) or math.isclose(
                100 * expected, value, abs_tol=tol
            )
            self.assertTrue(is_equal, "concentration not calculated accurately")
        except AttributeError as attribute_err:
            print(attribute_err)
            self.fail(
                f"It seems like {self.file_to_test} doesn't contain the function concentration_percent()"
            )
        except TypeError as type_err:
            print(type_err)
            self.fail(
                "It seems like the function concentration_percent isn't defined with the right number of input parameters"
            )

        self.assertIsNotNone(
            value,
            "It seems like the function concentration_percent() isn't returning a value",
        )
        self.assertIsInstance(
            value,
            float,
            f"It seems like the function concentration_percent() "
            f"is doesn't return the correct data type. It is currently "
            f"returning {type(value)}",
        )
        print("Perfect! concentration_percent() is there!")

    @weight(1)
    def test_logic(self):
        """Logic test intake_frequency()"""
        try:
            helper_func_name = self.student_code.concentration_percent.__name__
            function_to_test = self.student_code.intake_frequency
            self.assertTrue(
                uses_condition(function_to_test),
                "Oops, it seems like the active substance intake frequency is missing an important "
                "part of the algorithm the if statement!",
            )
            self.assertTrue(
                uses_loop(function_to_test),
                "Oops, it seems like the active substance intake frequency is missing an important "
                "part of the algorithm the loop!",
            )
            func_calls = get_func_calls(function_to_test)
            is_calling_helper = helper_func_name in func_calls
            self.assertTrue(
                is_calling_helper,
                f"The function {function_to_test.__name__}() is not calling {helper_func_name}()",
            )

        except AttributeError as a:
            self.fail(a)
        except TypeError as e:
            self.fail(e)
        print(
            "Great! You used all the statements and to determine the intake frequency"
        )

    @weight(1)
    def test_call_intake_frequency(self):
        """Accuracy Test intake_frequency()"""

        half_life = 5.5  # caffeine
        expected = math.log(20) * half_life / math.log(2)

        try:
            actual = self.student_code.intake_frequency(half_life=half_life)
            self.assertAlmostEqual(
                first=actual,
                second=expected,
                msg=f"Tested intake_frequency() with the caffeine's {half_life=} in hours. "
                f"Got {actual} but expected {round(expected)}",
                delta=1,
            )

        except AttributeError as a:
            self.fail(a)
        except TypeError as e:
            self.fail(e)
        print("Perfect! intake_frequency() is correctly calculated!")

    @weight(1)
    def test_intake_frequency_upper_bound(self):
        """Logic Test Upper bound frequency_intake()"""
        half_life = 1
        expected = math.ceil(math.log(20) * half_life / math.log(2))

        try:
            actual = self.student_code.intake_frequency(half_life=half_life)
            self.assertAlmostEqual(
                first=actual,
                second=expected,
                msg=f"Tested intake_frequency() with the caffeine's {half_life=} in hours."
                f" Got {actual} but expected {round(expected)}",
                delta=1,
            )
        except AttributeError as a:
            self.fail(a)
        except TypeError as e:
            self.fail(e)
        print(
            "Perfect! intake_frequency() takes into account the upper limit correctly"
        )


class TestQ3Evaluator(unittest.TestCase):
    def setUp(self):
        try:
            py_file, extension = splitext(files_to_test["func_file"])
            self.file_to_test = py_file
            self.student_code = __import__(py_file)
        except ModuleNotFoundError:
            self.fail(f"No file named {files_to_test}. Di you rename it? ")
        except Exception as e:
            self.fail(f"Unknown error {e}")

    @weight(1)
    def test_gcd_logic(self):
        """Logic Test gcd()"""
        try:
            function = self.student_code.gcd
            self.assertTrue(uses_loop(function), "gcd() isn't using a loop")
            self.assertTrue(
                uses_condition(function), "gcd() isn't using a conditional statement"
            )
        except Exception as e:
            self.fail(e)

    @weight(1)
    def test_gcd_accuracy(self):
        """Accuracy Test gcd()"""
        inputs = [(459, 322), (3, 15), (512, 1048)]
        expected_output = [1, 3, 8]
        try:
            for pair, expected in zip(inputs, expected_output):
                actual = self.student_code.gcd(*pair)
                self.assertEqual(
                    expected,
                    actual,
                    f"Incorrect gcd for {pair}. Expected {expected} Got {actual}",
                )
        except Exception as e:
            self.fail(e)


class TestQ4Evaluator(unittest.TestCase):
    def setUp(self):
        try:
            py_file, extension = splitext(files_to_test["func_file"])
            self.file_to_test = py_file
            self.student_code = __import__(py_file)
        except ModuleNotFoundError:
            self.fail(f"No file named {files_to_test}. Di you rename it? ")
        except Exception as e:
            self.fail(f"Unknown error {e}")

    def hex_area(self, a):
        """Helper to avoid repeating code"""
        return (3 / 2) * math.sqrt(3) * (a**2)

    @weight(1)
    def test_hex_area(self):
        """Accuracy Test hex_area()"""
        try:
            a = 1
            expected_area = self.hex_area(a)
            actual_area = self.student_code.hex_area(a)
            self.assertAlmostEqual(
                expected_area,
                actual_area,
                FLOAT_PRECISION_TOL,
                f"Hmm... the area of a hex of a={a}, should be {expected_area:.4f}, got {actual_area:.2f}",
            )
        except AttributeError as attribute_err:
            print(attribute_err)
            self.fail(
                f"It seems like {files_to_test[0]} doesn't contain the tested function "
            )
        print("Excellent, the area of one hex is correctly calculated")

    @weight(1)
    def test_using_loop(self):
        """Logic test check if green_area() uses loops"""
        try:
            function = self.student_code.green_area
            self.assertTrue(
                uses_loop(function),
                "The green area cannot be obtained without using a loop",
            )
        except Exception as e:
            self.fail(e)

    @weight(1)
    def test_green_area_accuracy(self):
        """Accuracy Test green_area()"""
        try:
            a0 = 2
            w = 3
            num_hex = 4
            first_green_idx = 2
            space_between_green = 4
            # generating the a_s of all green hexs sizes
            green_sides = [
                a0 + w * i for i in range(first_green_idx, num_hex, space_between_green)
            ]
            areas_green = [
                self.hex_area(a_green) - self.hex_area(a_green - w)
                for a_green in green_sides
            ]
            expected_total_area = sum(areas_green)
            actual_area = self.student_code.green_area(num_hex, a0, w)
            self.assertAlmostEqual(
                expected_total_area,
                actual_area,
                FLOAT_PRECISION_TOL,
                f"Hmm... the green area for {num_hex = }, {a0 = }, {w= } should be {expected_total_area} not {actual_area}",
            )
        except AttributeError as attribute_err:
            print(attribute_err)
            self.fail(
                f"It seems like {self.file_to_test} doesn't contain the tested function "
            )
        print("Great the green_area() does its job pretty well!")

    @weight(1)
    def test_varying_num_hex(self):
        """Logic Test 2 validating the num_hex is taken into account"""
        try:
            a0 = 2
            w = 3
            first_green_idx = 2
            space_between_green = 4
            for num_hex in range(5, 50):
                # generating the a_s of all green hexs sizes
                green_sides = [
                    a0 + w * i
                    for i in range(first_green_idx, num_hex, space_between_green)
                ]
                areas_green = [
                    self.hex_area(a_green) - self.hex_area(a_green - w)
                    for a_green in green_sides
                ]
                expected_total_area = sum(areas_green)
                actual_area = self.student_code.green_area(num_hex, a0, w)
                self.assertAlmostEqual(
                    expected_total_area,
                    actual_area,
                    FLOAT_PRECISION_TOL,
                    f"Hmm... the green area for {num_hex = }, {a0 = }, {w= } should be {expected_total_area} not {actual_area}",
                )
        except AttributeError as attribute_err:
            print(attribute_err)
            self.fail(
                f"It seems like {self.file_to_test} doesn't contain the tested function "
            )
        print("Great the green_area() does it's job pretty well!")
