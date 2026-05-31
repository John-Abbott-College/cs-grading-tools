import unittest
from config import DUE_DATE, CURRENT_DATE


@unittest.skipUnless(CURRENT_DATE < DUE_DATE, "deadline has not passed.")
class TestBeforeDeadline(unittest.TestCase):
    def test_not_a_test_just_a_message(self):
        """### Notes about the Gradescope Autograder ###"""

        print(f"""
Congratulations! You have submitted before the due date ({DUE_DATE}).
        """)
