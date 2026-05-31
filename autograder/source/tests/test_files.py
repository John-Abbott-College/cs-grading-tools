import unittest

from jac_cs_grading_tools.check_util import import_plus

from config import SUBMISSION_FILES

submission_file_errors: list[str] = []
for f in SUBMISSION_FILES:
    _, _, stderr, _ = import_plus(f)
    submission_file_errors += stderr


@unittest.skipUnless(len(submission_file_errors) > 0, str(submission_file_errors))
class TestImpossible(unittest.TestCase):
    longMessage: bool = False

    def test_no_errors(self):
        """Major errors prevent your code from being graded."""
        self.assertTrue(False, str(submission_file_errors))
