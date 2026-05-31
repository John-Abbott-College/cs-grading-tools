import unittest

from jac_cs_grading_tools.check_util import import_plus

from config import SUBMISSION_FILES

LIST_STR_PREFIX = "\n\n\t- "

submission_file_errors: list[str] = []
for f in SUBMISSION_FILES:
    try:
        _, _, stderr, _ = import_plus(f)
        submission_file_errors += stderr
    except Exception as e:
        submission_file_errors.append(f"{str(e)}")


@unittest.skipUnless(len(submission_file_errors) > 0, str(submission_file_errors))
class TestImpossible(unittest.TestCase):
    longMessage: bool = False

    def test_no_errors(self):
        """Major errors prevent your code from being graded correctly."""
        self.assertTrue(
            False, LIST_STR_PREFIX + LIST_STR_PREFIX.join(submission_file_errors)
        )
