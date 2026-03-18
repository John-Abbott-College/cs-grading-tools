#  Copyright (c) 2024 Ian Clement and Sandy Bultena.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#  License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not,
#  see <https://www.gnu.org/licenses/>.
from __future__ import annotations

import fnmatch
import json
import os.path
import subprocess
import sys
from typing import Optional

# -------------------------------------------------------------------------
# VERY IMPORTANT NOTE!!!
# -------------------------------------------------------------------------
"""
https://docs.pytest.org/en/7.1.x/how-to/usage.html
Calling pytest.main() will result in importing your tests and any modules that they import. 
Due to the caching mechanism of python’s import system, making subsequent calls to 
pytest.main() from the same process will not reflect changes to those files between the calls. 
For this reason, making multiple calls to pytest.main() from the same process (in order to 
re-run tests, for example) is not recommended.

Since we may run multiple tests with the same name, we need to run pytest as
a sub-process!
"""


# =============================================================================
# run tests in specific directory, return results
# =============================================================================
def run_pytest(where: str = "./") -> dict[str, UnitTest]:
    """
    Run unit tests in the specified directory and create a labeled dictionary of the results.
    """
    if not os.path.isdir(where):
        raise FileNotFoundError(f"Testing directory '{where}' does not exist")

    # this gets the current executable that is running, even if it is a virtual environment
    current_python = sys.executable

    # prepare to run the tests
    log_filename = "json_output.jsonl"
    args = [
        current_python,
        "-m",
        "pytest",
        os.path.abspath(where),
        "--timeout=5",
        f"--report-log={log_filename}",
    ]
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    ret_code = process.returncode
    if ret_code > 1:
        print(" ".join(args))
        message = f"{stdout.decode('utf8')}\n{stderr.decode('utf8')}"
        message = message.replace("\n", "\n\n")
        raise RuntimeError(message)

    # code: int = pytest.main([test_file_name, "-q", "--timeout=5", f"--report-log={test_log_file_name}"])
    return parse_test_output(log_filename)


def parse_test_output(log_filename) -> dict[str, UnitTest]:
    if True:
        results: dict[str, UnitTest] = {}

        with open(log_filename) as jsonl_file:
            for line in jsonl_file:
                node = json.loads(line)

                # we only care about "call" lines
                if "when" not in node or node["when"] != "call":
                    continue

                # create test result object from JSON
                test: UnitTest = UnitTest()
                test.name = node["location"][2]
                if node["outcome"] == "passed":
                    test.failed = False
                else:
                    test.failed = True
                    test.message = node["longrepr"]["reprcrash"]["message"]

                    # abbreviate the test messages
                    if "RuntimeError" in test.message:
                        # for runtime errors, put the line number in for extra info:
                        test.message = test.message.replace("RuntimeError: ", "")

                    else:
                        messages = []
                        for line in test.message.split("\n"):
                            if line.startswith("assert "):
                                break
                            messages.append(line)

                        test.message = "<br>".join(messages)
                        test.message = test.message.replace("AssertionError: ", "")

                results[test.name] = test

        return results


# =============================================================================
# Test Class
# =============================================================================
class UnitTest:
    """
    Represents a unit test, with truthy-falsy semantics
    """

    def __init__(
        self, name: str = "", failed: bool = False, message: str = "", size: int = 1
    ):
        self.name: str = name
        self.failed: bool = failed
        self.message: str = message
        self.size: int = size if failed else 0

    def __bool__(self) -> bool:
        return self.failed

    @staticmethod
    def _combine_messages(connective: str, message1: str, message2: str):
        """join two messages together with connective if both messages are non-blank,
        else just the non-blank message"""
        message1 = message1.strip()
        message2 = message2.strip()

        return (
            f" {connective} ".join((message1, message2))
            if message1 and message2
            else message1
            if message1
            else message2
            if message2
            else ""
        )

    def __add__(self, other: UnitTest) -> UnitTest:
        """Combine two tests such that the test fails if /either/ one fail.
        Basically failed = failed_1 OR failed_2"""
        return UnitTest(
            name=f"{self.name} + {other.name}",
            failed=bool(self) or bool(other),
            message=UnitTest._combine_messages("or", self.message, other.message),
            size=self.size + other.size,  # or? max(self.size, other.size)
        )

    def __mul__(self, other: UnitTest) -> UnitTest:
        """Combine two tests such that the test fails if /both/ one fail.
        Basically, failed = failed_1 AND failed_2"""
        return UnitTest(
            name=f"{self.name} x {other.name}",
            failed=bool(self) and bool(other),
            message=UnitTest._combine_messages("and", self.message, other.message),
            size=self.size + other.size,
        )

    def __sub__(self, other: UnitTest) -> UnitTest:
        """Combine two tests such that the test fails if self fails but other passes,i.e.: other /subsumes/ self."""
        if self and not other:
            return self
        else:
            return UnitTest(f"{self.name} - {other.name}", False, "")

    def __str__(self):
        return f"{self.name}: {'failed' if self.failed else 'passed'}"

    def __repr__(self):
        return str(self)

    @staticmethod
    def either(test1: UnitTest, test2: UnitTest) -> UnitTest:
        """Failed test if either tests fail."""
        return test1 + test2

    @staticmethod
    def both(test1: UnitTest, test2: UnitTest) -> UnitTest:
        """Failed test if both tests fail."""
        return test1 * test2

    @staticmethod
    def unless(test1: UnitTest, test2: UnitTest) -> UnitTest:
        """Fails if first test fails, unless second test fails."""
        return test1 - test2
