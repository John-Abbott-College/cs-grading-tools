# {py:mod}`grading_tools.rubric`

```{py:module} grading_tools.rubric
```

```{autodoc2-docstring} grading_tools.rubric
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`RubricDeduction <grading_tools.rubric.RubricDeduction>`
  - ```{autodoc2-docstring} grading_tools.rubric.RubricDeduction
    :summary:
    ```
* - {py:obj}`RubricSection <grading_tools.rubric.RubricSection>`
  - ```{autodoc2-docstring} grading_tools.rubric.RubricSection
    :summary:
    ```
* - {py:obj}`Rubric <grading_tools.rubric.Rubric>`
  - ```{autodoc2-docstring} grading_tools.rubric.Rubric
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SECTION <grading_tools.rubric.SECTION>`
  - ```{autodoc2-docstring} grading_tools.rubric.SECTION
    :summary:
    ```
* - {py:obj}`SECTION_WORTH <grading_tools.rubric.SECTION_WORTH>`
  - ```{autodoc2-docstring} grading_tools.rubric.SECTION_WORTH
    :summary:
    ```
* - {py:obj}`MINIMUM_POINTS <grading_tools.rubric.MINIMUM_POINTS>`
  - ```{autodoc2-docstring} grading_tools.rubric.MINIMUM_POINTS
    :summary:
    ```
* - {py:obj}`DEDUCTION_ID <grading_tools.rubric.DEDUCTION_ID>`
  - ```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_ID
    :summary:
    ```
* - {py:obj}`DEDUCTION_AMT <grading_tools.rubric.DEDUCTION_AMT>`
  - ```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_AMT
    :summary:
    ```
* - {py:obj}`DEDUCTION_FEEDBACK <grading_tools.rubric.DEDUCTION_FEEDBACK>`
  - ```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_FEEDBACK
    :summary:
    ```
* - {py:obj}`DEDUCTION_TESTS <grading_tools.rubric.DEDUCTION_TESTS>`
  - ```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_TESTS
    :summary:
    ```
* - {py:obj}`SKIP <grading_tools.rubric.SKIP>`
  - ```{autodoc2-docstring} grading_tools.rubric.SKIP
    :summary:
    ```
````

### API

````{py:data} SECTION
:canonical: grading_tools.rubric.SECTION
:value: >
   0

```{autodoc2-docstring} grading_tools.rubric.SECTION
```

````

````{py:data} SECTION_WORTH
:canonical: grading_tools.rubric.SECTION_WORTH
:value: >
   1

```{autodoc2-docstring} grading_tools.rubric.SECTION_WORTH
```

````

````{py:data} MINIMUM_POINTS
:canonical: grading_tools.rubric.MINIMUM_POINTS
:value: >
   2

```{autodoc2-docstring} grading_tools.rubric.MINIMUM_POINTS
```

````

````{py:data} DEDUCTION_ID
:canonical: grading_tools.rubric.DEDUCTION_ID
:value: >
   3

```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_ID
```

````

````{py:data} DEDUCTION_AMT
:canonical: grading_tools.rubric.DEDUCTION_AMT
:value: >
   4

```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_AMT
```

````

````{py:data} DEDUCTION_FEEDBACK
:canonical: grading_tools.rubric.DEDUCTION_FEEDBACK
:value: >
   5

```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_FEEDBACK
```

````

````{py:data} DEDUCTION_TESTS
:canonical: grading_tools.rubric.DEDUCTION_TESTS
:value: >
   6

```{autodoc2-docstring} grading_tools.rubric.DEDUCTION_TESTS
```

````

````{py:data} SKIP
:canonical: grading_tools.rubric.SKIP
:value: >
   7

```{autodoc2-docstring} grading_tools.rubric.SKIP
```

````

```{py:exception} RubricError()
:canonical: grading_tools.rubric.RubricError

Bases: {py:obj}`Exception`

```

`````{py:class} RubricDeduction
:canonical: grading_tools.rubric.RubricDeduction

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction
```

````{py:attribute} id
:canonical: grading_tools.rubric.RubricDeduction.id
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction.id
```

````

````{py:attribute} amount
:canonical: grading_tools.rubric.RubricDeduction.amount
:type: float
:value: >
   None

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction.amount
```

````

````{py:attribute} feedback
:canonical: grading_tools.rubric.RubricDeduction.feedback
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction.feedback
```

````

````{py:attribute} tests
:canonical: grading_tools.rubric.RubricDeduction.tests
:type: list[str]
:value: >
   'field(...)'

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction.tests
```

````

````{py:attribute} skip_tests
:canonical: grading_tools.rubric.RubricDeduction.skip_tests
:type: list[str]
:value: >
   'field(...)'

```{autodoc2-docstring} grading_tools.rubric.RubricDeduction.skip_tests
```

````

`````

`````{py:class} RubricSection
:canonical: grading_tools.rubric.RubricSection

```{autodoc2-docstring} grading_tools.rubric.RubricSection
```

````{py:attribute} name
:canonical: grading_tools.rubric.RubricSection.name
:type: str
:value: >
   None

```{autodoc2-docstring} grading_tools.rubric.RubricSection.name
```

````

````{py:attribute} worth
:canonical: grading_tools.rubric.RubricSection.worth
:type: float
:value: >
   None

```{autodoc2-docstring} grading_tools.rubric.RubricSection.worth
```

````

````{py:attribute} min_worth
:canonical: grading_tools.rubric.RubricSection.min_worth
:type: float
:value: >
   0.0

```{autodoc2-docstring} grading_tools.rubric.RubricSection.min_worth
```

````

````{py:attribute} contents
:canonical: grading_tools.rubric.RubricSection.contents
:type: list[grading_tools.rubric.RubricDeduction]
:value: >
   'field(...)'

```{autodoc2-docstring} grading_tools.rubric.RubricSection.contents
```

````

`````

`````{py:class} Rubric()
:canonical: grading_tools.rubric.Rubric

```{autodoc2-docstring} grading_tools.rubric.Rubric
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.rubric.Rubric.__init__
```

````{py:method} __iter__()
:canonical: grading_tools.rubric.Rubric.__iter__

```{autodoc2-docstring} grading_tools.rubric.Rubric.__iter__
```

````

````{py:method} read_from_csv(filename: str) -> grading_tools.rubric.Rubric
:canonical: grading_tools.rubric.Rubric.read_from_csv

```{autodoc2-docstring} grading_tools.rubric.Rubric.read_from_csv
```

````

`````
