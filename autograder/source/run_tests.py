from pathlib import Path
import unittest
import pytest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
from utilities import turtle_comment_out_mainloops
from config import (
    RESULTS_JSON,
    PYTEST_RESULTS_JSON,
    SOURCE_PREFIX,
    SUBMISSION_PREFIX,
    SUBMISSION_FILES,
    IS_GRAPHICAL,
)

import sys

sys.path.append(SUBMISSION_PREFIX)


def post_processor_sort_by_name(json_data):
    """Used to ensure that tests are presented in alphabetical order on Gradescope."""
    json_data["tests"] = sorted(json_data["tests"], key=lambda d: d["name"])


if __name__ == "__main__":
    if IS_GRAPHICAL:
        turtle_comment_out_mainloops(SUBMISSION_FILES)

    if Path(f"{SOURCE_PREFIX}/pytests").is_dir():
        Path(PYTEST_RESULTS_JSON).parent.mkdir(parents=True, exist_ok=True)
        with Path(PYTEST_RESULTS_JSON).open("w") as f:
            _ = pytest.main(
                [
                    f"{SOURCE_PREFIX}/pytests",
                    f"--report-log={PYTEST_RESULTS_JSON}",
                ]
            )

    suite = unittest.defaultTestLoader.discover(f"{SOURCE_PREFIX}/tests")
    Path(RESULTS_JSON).parent.mkdir(parents=True, exist_ok=True)
    with Path(RESULTS_JSON).open("w") as f:
        JSONTestRunner(
            buffer=True,
            stream=f,
            post_processor=post_processor_sort_by_name,
        ).run(suite)
