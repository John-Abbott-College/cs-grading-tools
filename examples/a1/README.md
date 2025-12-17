# Auto Grading Library for Michael's Fall 2025 Asg1

Adapted from the main README authored by Ian and Sandy

## File preparation

Student files should come from LEA, where the **Select only the latest submission of each student** and the **Group by directory and extract the compressed files** options have been chosen.

Place the student folders in a common grading directory, alongside the `AutoGrading` folder, like so:

```
├── AutoGrading
│   ├── check_util.py
│   ├── evaluation.py
│   ├── feedback_utils.py
│   ├── grading.py
│   ├── zip_feedback.sh
├── A1-grading-dir
│   ├── LastName1_1234567_Assignment_1_Submitted_on_2025-11-11_11h11m11s
│   │   ├── question_1_fix_me.py
│   │   ├── question_2_formatting.py
│   │   ├── question_3_toy_packing_plant.py
│   │   ├── question_4_tariffs.py
│   │   └── question_5_recipe.py
│   ├── LastName2_7654321_Assignment_1_Submitted_on_2025-11-11_11h11m11s
│   │   │   ├── etc.
```

## Creating tests

Create your test suite using `pytest`. For this assignment, this has been done in the `evaluation.py` file.

```
├── evaluation.py             pytest entrypoint
├── grading.py                grading domain class definitions (Student, Deduction, etc.)
├── check_util.py             additional testing tools
├── feedback_utils.py         produces the rubric markdown for each student
├── zip_feedback.sh           shell script to prepare Assignments.zip feedback collection
```

For every `assert` in your tests, if it is followed by a string, that string will be inserted into the user's feedback.

## Grade by running the tests

Navigate to each student directory:

```shell
$ python ../Autograding/evaluation.py
... follow the prompts ...
... if everything works:
Feedback generated: feedback_file=1234567_LastName.md
```

## Prepare Assignments.zip

From the autograding directory:

```shell
$ ./zip_feedback.sh ../A1-grading-dir

Creating A1-grading-dir/LastName1_1234567_Assignment_1_Submitted_on_2025-11-11_11h11m11s/1234567_LastName1.pdf...
Creating A1-grading-dir/LastName1_1234567_Assignment_1_Submitted_on_2025-11-11_11h11m11s/7654321_LastName2.pdf...
... etc ...
  adding: 1234567_LastName1.pdf (stored 0%)
  adding: 7654321_LastName2.pdf (deflated 2%)
Archive:  ./Assignments.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
   169449  10-22-2025 16:47   1234567_LastName1.pdf

... there would normally be more files than this ...

   169449  10-22-2025 16:47   7654321_LastName2.pdf
---------                     -------
   338318                     2 files
```

## Rubric

The rubric *csv* file has the following columns

* **Section**
  * Starts a new section if this column is not empty with the name that is in this column
* **S_Worth**
  * The maximum worth or value of this section
* **Min Points**
  * The minimum points that this section is allowed to be 
    * For example, I tend to give no points for code quality, but allow the value of Code Quality to be as low as 10% of the total grade
    * Typically, min points will be zero
* **Deduction ID**, 
  * Hopefully a unique *id* for this particular deduction (deductions belong to sections)
* **Deduction amt**
  * How much to deduct if the tests fail
* **Feedback**
  * What is to be written if the test fails
* **Tests**
  * What `pytest` tests are used to determine pass or fail
  * If no tests are specified, then the tester will be prompted for a pass/fail response
* **Skip**
  * If the tests fail, what future test results should be ignored (space separated deduction ID numbers)
