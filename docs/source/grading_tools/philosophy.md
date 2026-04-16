# Autograder

## Philosophy

**It is not a one-to-one mapping between tests and grades.**

For example, if code cannot read the input `csv` file, then the rest of the code can certainly not pass any of the other tests.  

**Students should not be penalized doubly for failing tests**

Again, as in the previous example, the student should lose grades if the student cannot read the file, but not for all the subsequent failing tests.

## Installation

Goto [python-autograder]()[https://github.com/ianclement/python-autograder) and read the installation instructions in the `README` file.

## Example Usage

### Student Code

```python
from __future__ import annotations
import math

class Point:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def dist_linear(self, other: Point) -> float:
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.x - other.y, 2))

    def dist_city_block(self, other: Point) -> float:
        return abs(self.x - other.x) * abs(self.y - other.y)

    def move(self, dx: int, dy: int):
        self._x += dx
        self._y += dy

    def add(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.x)

    def __str__(self):
        return f"({self.x},{self.y})"
```



### Grouping Assessments

How will you be grading?

For this student's code, the assessment will be divided into two:

* Distance Calculation 
* Point Operations 

### Create the test file

For each assessment group, divide the tests using comments that start with: `# SECTION: `

```python
import math
from student_code import Point
import pytest

@pytest.fixture
def data_x() -> list[Point]:
    return [Point(x + 1, 1) for x in range(10)]


@pytest.fixture
def data_y() -> list[Point]:
    return [Point(x + 1, 1) for x in range(10)]

# ============================================================================
# SECTION: Distance Calculation
# ============================================================================

def test_dist_linear(data_x: list[Point]):
    p0 = Point(0, 0)
    ans_sqrt2 = data_x[0].dist_linear(p0)
    ans_sqrt5 = data_x[1].dist_linear(p0)
    ans_sqrt10 = data_x[2].dist_linear(p0)
    assert math.sqrt(2) == pytest.approx(ans_sqrt2, 0.001), \
        f"linear distance between {data_x[0]} and {p0} "+\
        f"should be ~{math.sqrt(2):.3f}, you calculated {ans_sqrt2:.3f}"
    assert math.sqrt(5) == pytest.approx(ans_sqrt5, 0.001), \
        f"linear distance between {data_x[1]} and {p0} should be "+\
        f"~{math.sqrt(5):.3f}, you calculated {ans_sqrt5:.3f}"
    assert math.sqrt(10) == pytest.approx(data_x[2].dist_linear(Point(0, 0)), 0.001), \
        f"linear distance between {data_x[2]} and {p0} "+\
        f"should be ~{math.sqrt(10):.3f}, you calculated {ans_sqrt10:.3f}"


def test_dist_city_block(data_x: list[Point]):
    p1 = Point(1,1)
    ans_0 = data_x[0].dist_city_block(p1)
    ans_1 = data_x[1].dist_city_block(p1)
    ans_2 = data_x[2].dist_city_block(p1)
    assert 0 == ans_0, \
    			f"city distance between {data_x[0]} and {p1} should be {0}, you calculated {ans_0}"
    assert 1 == ans_1, \
    			f"city distance between {data_x[1]} and {p1} should be {1}, you calculated {ans_1}"
    assert 2 == ans_2, \
    			f"city distance between {data_x[2]} and {p1} should be {2}, you calculated {ans_2}"

# ============================================================================
# SECTION: Point Operations
# ============================================================================

def test_point_addition():
    p: Point = Point(1, 2).add(Point(3, 4))
    assert p.x == 4 and p.y == 6, \
        f"Problem adding points. For example (1, 2) + (3, 4) "+\
         "should be (4, 6) but your code gives ({p.x}, {p.y})."

```



### Create the evaluation file

From the command line, run the following:

```bash
python3 -m autograder.generate_evaluation_code_from_test_file evaluation.py test_file.py 
```

This will create a file called `evaluation.py` based on what is in the test file.

### Understanding the `evaluation` file

**basic setup**

* imports the required modules

  ```python
  from autograder import Evaluation, UnitTest, unit_test, StudentInfo, Processor
  from autograder import options
  ```

* set some default options

  * `options.set_get_student_info_from`:  where to collect the student information

    * `options.ExtractStudentInfoFrom.LEA` - gets the student's username, id from the filename that LEA outputs (*default*)

    * `options.ExtractStudentInfoFrom.LEA` - gets the student's username, id from the filename that LEA outputs, and extracts the student's first name by read a csv file (NOT IMPLEMENTED)
  
  * `options.set_output_type`: what will be the file format of the evaluation results
  
    * `options.OutputType.MARKDOWN` (*default*)
    * `options.OutputType.LATEX` (*not implemented well*)
  
  * `options.set_unit_test_type`: what type of unit tests are you running?
  
    * `options.UNIT_TEST_TYPE.PYTEST`: runs `pytest *.py` (*default*)
  
  ```python
  options.set_get_student_info_from(options.ExtractStudentInfoFrom.LEA)
  options.set_output_type(options.OutputType.MARKDOWN)
  options.set_unit_test_type(options.UNIT_TEST_TYPE.PYTEST)
  ```
* define the location of files
  * source directory containing the test files (required)
  * assignment directory containing the student code (required if analyzing a single student)
  * student source directory containing all the student code for all students downloaded from LEA (required if doing batch grading)
* other files
  * any files that need to be copied from the test directory that are not defined by `test_*.py`

```python
test_source_directory = TODO
assignment_directory = TODO
# student_source_directory = TODO
other_files = []
```

**Evaluation**

```python
# =============================================================================
# run unit-tests and evaluate results
# =============================================================================
def evaluate(where) -> Evaluation:
```

The `evaluate` function, which is a function passed to the `Processor` init function, starts by first defining the total that this assessment will be graded on. (you must replace the  `TODO_total_grade_value` with the total assessment value)

The location of where the test are executed is passed into this method by the `Processor` instance.

```python
    evaluation: Evaluation = Evaluation('Assignment',  TODO_total_grade_value)

    print(f"Running tests: {where}")
```

Ex:  `def test_dist_linear(data_x: list[Point]):` would result in a valid key `test_dist_linear` in the ``results` document.

All of the unit tests are executed, but if there is a fatal error, the feedback for this failure is documented, and the evaluation is terminated.

Note that the `code` is an arbitrary number, and can be changed to suit your own needs.

```python
    
    # -------------------------------------------------------------------------
    # if you can't run the unit tests, fail miserable and bail-out
    # -------------------------------------------------------------------------
    try:
        results: dict[str, UnitTest] = unit_test.run_pytest(where)
    except RuntimeError:
        message:str = e.args[0]
        evaluation.start_section("Fatal Error", evaluation.total)
        evaluation.deduction(code='99',
                             test=UnitTest(name="test_file_can_run", failed=True),
                             weight=evaluation.total,
                             feedback="FATAL ERROR\n\n"+message,
                             requires_human_review=True
                             )
        return evaluation

```

The results of the unit tests are stored in a dictionary `results`, where the key is the name of the function that executed the test.

```python
    # Unit Tests
    test_dist_linear: UnitTest = results['test_dist_linear']
    test_dist_city_block: UnitTest = results['test_dist_city_block']
    test_point_addition: UnitTest = results['test_point_addition']

```

**Evaluation of test results**

Tests are organized by section.  For each test in a section, an evaluation `deduction` is created which takes the following information:

* `code` An arbitrary number which can be modified for your own purposes in the feedback file
* `weight` How much will be deducted from the grade if this test failed
* `feedback` What will be printed to the feedback file as an explanation for the deduction
* `requires_human_review`: In the csv file that is created as part of the feedback, this boolean will appear there.  It is used to indicate to the grader that if this test failed, the grader needs to review the assessment manually.
  * If not set, defaults to `False`


```python

    # Evaluation
    evaluation.start_section('Distance Calculation', TODO_section_total_grade)
    evaluation.deduction(code='0.0',
                         test=test_dist_linear,
                         weight=TODO,
                         feedback=results['test_dist_linear'].message,
                         requires_human_review=False,
                         )
    evaluation.deduction(code='0.1',
                         test=test_dist_city_block,
                         weight=TODO,
                         feedback=results['test_dist_city_block'].message,
                         requires_human_review=False,
                         )

    evaluation.start_section('Point Operations', TODO_section_total_grade)
    evaluation.deduction(code='1.0',
                         test=test_point_addition,
                         weight=TODO,
                         feedback=results['test_point_addition'].message,
                         requires_human_review=False,
                         )
    return evaluation
```

**Running tests **

The `autograder` gives options to evaluate a single student, or all students

```python
# =============================================================================
# define files etc for processing student evaluations
# =============================================================================
def set_up_processor(test_source_dir: str,
                     other_required_files: list[str]) -> Processor:
    return Processor(evaluator=evaluate,
                     test_files=unit_test.find_all_test_files(test_source_dir),
                     files_to_test=["*.py"],
                     other_required_files=other_files)

# =============================================================================
# entry point
# =============================================================================
if __name__ == "__main__":
    processor = set_up_processor(test_source_dir=test_source_directory,
                                 other_required_files=other_files)
                                 
    processor.run_tests_for_each_student(assignment_directory)
    
    # processor.run_tests_for_single_student(
    #                 StudentInfo(path_to_student_folder=student_source_directory)
    #                 )
```

### Modifying the Evaluation File

Where necessary, edit the evaluation file by replaceing the appropriate `TODO`s with valid data.

However, the assumption is that the grade deductions are not always a one-to-one match between test and deduction.  In this example, we want:

* If the student fails the tests for both the linear and city block calculations, the deduction should be `15` 
* If the student fails the linear calculation, but not the city calculation, the deduction should be `10`
* if the student fails the city calculation, but not the linear calculation, the deduction should be `10`.

To do this, we would modify the "Distance Calculation" section of the  evaluation to look like this:

Note that using `UnitTest.both` and `UnitTest.unless` will create new test objects, and defined the `message` accordingly.

```python
    test_linear_and_city_block = UnitTest.both(test_dist_linear, test_dist_city_block)
    test_just_linear = UnitTest.unless(test_dist_linear, test_linear_and_city_block)
    test_just_city_block = UnitTest.unless(test_dist_city_block, test_linear_and_city_block)

    evaluation.start_section('Distance Calculation', 15)

    evaluation.deduction(code="4",
                         test=test_linear_and_city_block,
                         weight=10,
                         feedback=test_linear_and_city_block.message,
                         requires_human_review=False,
                         )

    evaluation.deduction(code="2",
                         test=test_just_linear,
                         weight=7.5,
                         feedback=test_just_linear.message
                         )
    evaluation.deduction(code="3",
                         test=test_just_city_block,
                         weight=7.5,
                         feedback=test_just_city_block.message
                         )


```

### Autograder Output

If I run the modified evaluation file for a single student, it will create a feedback file (markdown).


> # Assignment [5.0/20]
> 
> |           |                                     |
> |-----------|-------------------------------------|
> | StudentID | 0000                                |
> | Name      |                               |
> | Submitted | 2000-01-01 00:00:00                              |
> | Late      | - 0.00   ( 0.00 days)         |
> | Grade     | 5.00 -  0.00 |
> | Final Grade     | 5.00 out of 20 ( 25.00%) |
> 
> **Comment**
> 
> See me and we can go over this assignment.
> 
> ### Results:
> * **Distance Calculation [5.0/15]**
>   * linear distance between (2,1) and (0,0) should be ~2.236, you calculated 2.828 and city distance between (2,1) and (1,1) should be 1, you calculated 0  [-10.0]
> * **Point Operations [0.0/5]**
>   * Problem adding points. For example (1, 2) + (3, 4) should be (4, 6) but your code gives ({p.x}, {p.y}).  [-5.0]



