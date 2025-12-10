---
authors:
  - sandy_bultena
  - ian_clement
  - michael_haaf
---

# Auto Grading Library

## How To

<!-- TODO: installation instructions -->

### Student files

Student files should come from LEA, where the **Select only the latest submission of each student** and the **Group by directory and extract the compressed files** options have been chosen. If you don't want to do this, then the only file that really needs to be modified is the `generate_feedback.py` file.

### Testing

Create your test suite using `pytest`. There are additional testing tools available in `check_utils.py`. See _References_ for a list of stuff that should make your life easier.

For every `assert` in your tests, if it is followed by a string, that string will be inserted into the user's feedback

### Rubric

The rubric _csv_ file has the following columns

- **Section**
  - Starts a new section if this column is not empty with the name that is in this column
- **S_Worth**
  - The maximum worth or value of this section
- **Min Points**
  - The minimum points that this section is allowed to be
    - For example, I tend to give no points for code quality, but allow the value of Code Quality to be as low as 10% of the total grade
    - Typically, min points will be zero
- **Deduction ID**,
  - Hopefully a unique _id_ for this particular deduction (deductions belong to sections)
- **Deduction amt**
  - How much to deduct if the tests fail
- **Feedback**
  - What is to be written if the test fails
- **Tests**
  - What `pytest` tests are used to determine pass or fail
  - If no tests are specified, then the tester will be prompted for a pass/fail response
- **Skip**
  - If the tests fail, what future test results should be ignored (space separated deduction ID numbers)

## Example Usage (with required IO)

**Student Code `hotel.py`**

```python
# price of hotel base on number of kids
basic_price = 100
additional_for_2_kids_or_less = 20
each_additional_kid = 15

num_kids = int(input("Number of kids staying with you? "))
Total = basic_price
if num_kids > 0:
    Total += 20
if num_kids > 2:
    Total += (num_kids - 2)*15
print(f"The price of your hotel is {Total}")

def FunctionWithBad_Naming():
    pass
```

**pytest** (filename _must_ start with `test_`)

```python
import re
import pytest

from grading_tools.check_util import (errors_and_warnings, style_invalid_naming_style,
                                      get_linter_info, import_plus,
                                      import_file_with_dummy_dummy_inputs)

hotel_linter = get_linter_info("hotel.py")


def test_warnings_hotel():
    e, w = errors_and_warnings(hotel_linter)
    assert len(w) == 0, "\n".join(w)


def test_errors_hotel():
    e, w = errors_and_warnings(hotel_linter)
    assert len(e) == 0, "\n".join(e)


def test_naming_conventions_hotel():
    e = style_invalid_naming_style(hotel_linter)
    # ignore constants are supposed to be upper case
    e = list(filter(lambda x: "UPPER_CASE" not in x, e))
    assert len(e) == 0, "\n".join(e)


def test_warnings_hotel_import():
    module, stdout, stderr, source = import_file_with_dummy_dummy_inputs("hotel.py")
    assert len(stderr) == 0, "COULD NOT IMPORT hotel:\n" + "\n".join(stderr)


def test_hotel_with_5_kids():
    try:
        module, stdout, stderr, source = import_file_with_dummy_dummy_inputs("hotel.py")
    except ImportError:
        pytest.xfail("cannot import module")

    module, stdout, stderr, source = import_plus("hotel.py", ["5"])

    assert re.search(r"(^|\s)165(,|\s|$)", stdout[0]), (f"For 5 kids the total price is 165, "
                                                        f"your code printed: \n{'\n'.join(stdout)}")


def test_hotel_no_hard_coding():
    """change the default price, etc """
    try:
        module, stdout, stderr, source = import_file_with_dummy_dummy_inputs("hotel.py")
    except ImportError:
        pytest.xfail("cannot import module")

    def modify(source_code: str) -> str:
        new_code = []
        for line in source_code.split("\n"):
            if line.startswith("basic_price"):
                new_code.append("basic_price = 115")
            elif line.startswith("additional_for_2_kids_or_less"):
                new_code.append("additional_for_2_kids_or_less = 25")
            elif line.startswith("each_additional_kid"):
                new_code.append("each_additional_kid = 20")
            else:
                new_code.append(line)
        return "\n".join(new_code)

    module, stdout, stderr, source = import_plus("hotel.py", "5", modify)
    assert re.search(r"(^|\s)200(,|\s|$)", stdout[0]), (f"If the basic price is 115, and the additional kids is 25, "
                                                        f"and each additional kid is 20, then the final cost should be 200, "
                                                        f"your code printed: \n{'\n'.join(stdout)}")

```

**rubric**

```text
Section, S_Worth, Min Points, Deduction ID, Deduction amt, Feedback, Tests, Skip,
Code Quality, 0, -3
,,,1, 1, You have the following warnings..., test_warnings_hotel,
,,,2, 2, You have the following errors..., test_errors_hotel,
,,,3, 0.5, You must follow the proper naming conventions..., test_naming_conventions_hotel,
Functionality, 10, 0
,,,4, 10, The file cannot be imported, test_hotel_import, 5 6 ,
,,,5, 10, Invalid calculation,test_hotel_with_5_kids
,,,6, 5, Hard coding values,test_hotel_no_hard_coding

```

**generate*feedback (\_boilerplate*)**

... I guess since most of this is boilerplate, we could create a new function in the library... but for now, this is what I got.

```python
from datetime import datetime
import sys
import os
import pathlib
import posixpath

from grading_tools.unit_test import run_pytest
from grading_tools.feedback_utils import get_student_info_from_lea, give_feedback, Student
from grading_tools.run_tests import run_tests
from grading_tools.rubric import Rubric

# =============================================================================
# info
# =============================================================================
due_date = datetime(2025, 4, 2, 8)
files = ["hotel.py"]
rubric = Rubric().read_from_csv("rubric.csv")

# =============================================================================
# make soft links from student dir to testing directory
# =============================================================================
if len(sys.argv) == 1:
    student_dir = input("Student dir? ")
else:
    student_dir = sys.argv[1]

for file in files:
    if os.path.exists(file) or os.path.islink(file):
        os.remove(file)
    for p in pathlib.Path(student_dir).rglob(file):
        pname = posixpath.join(p)
        if "MACOS" not in pname:
            os.symlink(pname, file)
            break

# =============================================================================
# get student from directory name (assumes output from LEA
# =============================================================================
pathname = os.path.abspath(student_dir)
dirs = pathname.split(os.sep)
student: Student = get_student_info_from_lea(dirs[-1], due_date)


# =============================================================================
# run py_tests
# =============================================================================
test_results = run_pytest()

grading = run_tests(rubric, test_results)
grading.days_late = student.days_late
give_feedback(student, grading, files)

```

**Generated Output**

````text
#  [4.5/10.0]

|           |                                     |
|-----------|-------------------------------------|
| StudentID | 1234567                                |
| Name      | LastName                              |
| Submitted | 2025-03-28 14:04:19                              |
| Late      | - 0.00   ( 0.00 days)         |
| Grade     | 4.50 -  0.00 |
| Final Grade     | 4.50 out of 10.0 ( 50.00%) |

**Comment**

See me and we can go over this assignment.

### Results:
* [`  -0.50/0.00`] **Code Quality**
  * `[- 0.50]`   You must follow the proper naming conventions...
     hotel.py: 14: Function name "FunctionWithBad_Naming" doesn't conform to snake_case naming style
* [`  5.00/10.00`] **Functionality**
  * `[- 5.00]`   Hard coding values
    If the basic price is 115, and the additional kids is 25, and each additional kid is 20, then the final cost should be 200, your code printed:
    Number of kids staying with you? The price of your hotel is 180

## Code

### hotel.py
```python
# price of hotel base on number of kids
basic_price = 100
additional_for_2_kids_or_less = 20
each_additional_kid = 15

num_kids = int(input("Number of kids staying with you? "))
Total = basic_price
if num_kids > 0:
    Total += 20
if num_kids > 2:
    Total += (num_kids - 2)*15
print(f"The price of your hotel is {Total}")

def FunctionWithBad_Naming():
    pass
```

````
