import unittest

from jac_cs_grading_tools.check_util import import_plus

from config import SUBMISSION_FILES


_, _, stderr, _ = import_plus(SUBMISSION_FILES)


@unittest.skipUnless(len(stderr) > 0, str(stderr))
class TestImpossible(unittest.TestCase):
    longMessage: bool = False

    def test_no_errors(self):
        """Major errors prevent your code from being graded."""
        self.assertTrue(False, str(stderr))
