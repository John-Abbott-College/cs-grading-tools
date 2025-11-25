# {py:mod}`grading_tools.grading`

```{py:module} grading_tools.grading
```

```{autodoc2-docstring} grading_tools.grading
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Grading <grading_tools.grading.Grading>`
  - ```{autodoc2-docstring} grading_tools.grading.Grading
    :summary:
    ```
* - {py:obj}`Section <grading_tools.grading.Section>`
  - ```{autodoc2-docstring} grading_tools.grading.Section
    :summary:
    ```
* - {py:obj}`Deductions <grading_tools.grading.Deductions>`
  - ```{autodoc2-docstring} grading_tools.grading.Deductions
    :summary:
    ```
````

### API

`````{py:class} Grading()
:canonical: grading_tools.grading.Grading

```{autodoc2-docstring} grading_tools.grading.Grading
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.grading.Grading.__init__
```

````{py:method} add_section(name: str, max_grade: float, min_grade: float = 0) -> grading_tools.grading.Section
:canonical: grading_tools.grading.Grading.add_section

```{autodoc2-docstring} grading_tools.grading.Grading.add_section
```

````

````{py:property} sections
:canonical: grading_tools.grading.Grading.sections

```{autodoc2-docstring} grading_tools.grading.Grading.sections
```

````

````{py:method} grade() -> float
:canonical: grading_tools.grading.Grading.grade

```{autodoc2-docstring} grading_tools.grading.Grading.grade
```

````

````{py:method} out_of() -> int
:canonical: grading_tools.grading.Grading.out_of

```{autodoc2-docstring} grading_tools.grading.Grading.out_of
```

````

````{py:method} late_penalty() -> float
:canonical: grading_tools.grading.Grading.late_penalty

```{autodoc2-docstring} grading_tools.grading.Grading.late_penalty
```

````

````{py:method} __str__()
:canonical: grading_tools.grading.Grading.__str__

````

````{py:method} serialize()
:canonical: grading_tools.grading.Grading.serialize

```{autodoc2-docstring} grading_tools.grading.Grading.serialize
```

````

````{py:method} de_serialize(filename)
:canonical: grading_tools.grading.Grading.de_serialize
:classmethod:

```{autodoc2-docstring} grading_tools.grading.Grading.de_serialize
```

````

`````

`````{py:class} Section(name, max_grade: float, min_grade: float = 0.0)
:canonical: grading_tools.grading.Section

```{autodoc2-docstring} grading_tools.grading.Section
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.grading.Section.__init__
```

````{py:attribute} separator
:canonical: grading_tools.grading.Section.separator
:value: >
   '|'

```{autodoc2-docstring} grading_tools.grading.Section.separator
```

````

````{py:method} ask_question(question, response, grade: float) -> str
:canonical: grading_tools.grading.Section.ask_question

```{autodoc2-docstring} grading_tools.grading.Section.ask_question
```

````

````{py:method} ask_question_with_feedback(question, grade: float) -> str
:canonical: grading_tools.grading.Section.ask_question_with_feedback

```{autodoc2-docstring} grading_tools.grading.Section.ask_question_with_feedback
```

````

````{py:method} ask_question_with_variable_grade(question) -> str
:canonical: grading_tools.grading.Section.ask_question_with_variable_grade

```{autodoc2-docstring} grading_tools.grading.Section.ask_question_with_variable_grade
```

````

````{py:method} add_result(response, grade: float)
:canonical: grading_tools.grading.Section.add_result

```{autodoc2-docstring} grading_tools.grading.Section.add_result
```

````

````{py:method} grade() -> float
:canonical: grading_tools.grading.Section.grade

```{autodoc2-docstring} grading_tools.grading.Section.grade
```

````

````{py:method} clear_deductions()
:canonical: grading_tools.grading.Section.clear_deductions

```{autodoc2-docstring} grading_tools.grading.Section.clear_deductions
```

````

````{py:method} __str__()
:canonical: grading_tools.grading.Section.__str__

````

`````

`````{py:class} Deductions
:canonical: grading_tools.grading.Deductions

```{autodoc2-docstring} grading_tools.grading.Deductions
```

````{py:attribute} deduction
:canonical: grading_tools.grading.Deductions.deduction
:type: float
:value: >
   None

```{autodoc2-docstring} grading_tools.grading.Deductions.deduction
```

````

````{py:attribute} feedback
:canonical: grading_tools.grading.Deductions.feedback
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.grading.Deductions.feedback
```

````

````{py:method} __str__()
:canonical: grading_tools.grading.Deductions.__str__

````

`````
