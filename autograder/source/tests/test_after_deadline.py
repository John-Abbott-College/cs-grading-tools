import unittest
from config import DUE_DATE, CURRENT_DATE


@unittest.skipUnless(CURRENT_DATE > DUE_DATE, "deadline passed.")
class TestAfterDeadline(unittest.TestCase):
    def test_not_a_test_just_a_message(self):
        """### Notes about the Gradescope Autograder ###"""

        print(f"""
The initial due date ({DUE_DATE}) has now passed.
        """)
