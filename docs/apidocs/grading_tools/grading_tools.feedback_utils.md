# {py:mod}`grading_tools.feedback_utils`

```{py:module} grading_tools.feedback_utils
```

```{autodoc2-docstring} grading_tools.feedback_utils
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Student <grading_tools.feedback_utils.Student>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.Student
    :summary:
    ```
* - {py:obj}`MarkDownFormat <grading_tools.feedback_utils.MarkDownFormat>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_student_info_from_lea <grading_tools.feedback_utils.get_student_info_from_lea>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.get_student_info_from_lea
    :summary:
    ```
* - {py:obj}`give_feedback <grading_tools.feedback_utils.give_feedback>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.give_feedback
    :summary:
    ```
* - {py:obj}`print_evaluation <grading_tools.feedback_utils.print_evaluation>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.print_evaluation
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`OUTPUT_COMMENTS <grading_tools.feedback_utils.OUTPUT_COMMENTS>`
  - ```{autodoc2-docstring} grading_tools.feedback_utils.OUTPUT_COMMENTS
    :summary:
    ```
````

### API

````{py:data} OUTPUT_COMMENTS
:canonical: grading_tools.feedback_utils.OUTPUT_COMMENTS
:type: list[tuple[range, str]]
:value: >
   [(), (), (), (), (), ()]

```{autodoc2-docstring} grading_tools.feedback_utils.OUTPUT_COMMENTS
```

````

`````{py:class} Student
:canonical: grading_tools.feedback_utils.Student

```{autodoc2-docstring} grading_tools.feedback_utils.Student
```

````{py:attribute} id
:canonical: grading_tools.feedback_utils.Student.id
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.feedback_utils.Student.id
```

````

````{py:attribute} name
:canonical: grading_tools.feedback_utils.Student.name
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.feedback_utils.Student.name
```

````

````{py:attribute} submission_date
:canonical: grading_tools.feedback_utils.Student.submission_date
:type: datetime.datetime
:value: >
   None

```{autodoc2-docstring} grading_tools.feedback_utils.Student.submission_date
```

````

````{py:attribute} days_late
:canonical: grading_tools.feedback_utils.Student.days_late
:type: float
:value: >
   None

```{autodoc2-docstring} grading_tools.feedback_utils.Student.days_late
```

````

`````

````{py:function} get_student_info_from_lea(folder_name: str, due_date: typing.Optional[datetime.datetime] = None) -> grading_tools.feedback_utils.Student
:canonical: grading_tools.feedback_utils.get_student_info_from_lea

```{autodoc2-docstring} grading_tools.feedback_utils.get_student_info_from_lea
```
````

````{py:function} give_feedback(student: grading_tools.feedback_utils.Student, evaluation: grading_tools.grading.Grading, source_files: list[str] = None)
:canonical: grading_tools.feedback_utils.give_feedback

```{autodoc2-docstring} grading_tools.feedback_utils.give_feedback
```
````

````{py:function} print_evaluation(student: grading_tools.feedback_utils.Student, evaluation: grading_tools.grading.Grading, file: typing.TextIO = sys.stdout, source_files=None)
:canonical: grading_tools.feedback_utils.print_evaluation

```{autodoc2-docstring} grading_tools.feedback_utils.print_evaluation
```
````

`````{py:class} MarkDownFormat
:canonical: grading_tools.feedback_utils.MarkDownFormat

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat
```

````{py:method} header()
:canonical: grading_tools.feedback_utils.MarkDownFormat.header
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.header
```

````

````{py:method} title(title: str, score: float, weight: int) -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.title
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.title
```

````

````{py:method} student_info(student: grading_tools.feedback_utils.Student, evaluation: grading_tools.grading.Grading, comment: str) -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.student_info
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.student_info
```

````

````{py:method} section_header(name: str, score: float, weight: float) -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.section_header
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.section_header
```

````

````{py:method} deduction(feedback: str, weight: float) -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.deduction
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.deduction
```

````

````{py:method} result_header() -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.result_header
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.result_header
```

````

````{py:method} code_header() -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.code_header
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.code_header
```

````

````{py:method} code_file(filename: str, code: str) -> str
:canonical: grading_tools.feedback_utils.MarkDownFormat.code_file
:staticmethod:

```{autodoc2-docstring} grading_tools.feedback_utils.MarkDownFormat.code_file
```

````

`````
