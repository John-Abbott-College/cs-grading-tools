# {py:mod}`grading_tools.unit_test`

```{py:module} grading_tools.unit_test
```

```{autodoc2-docstring} grading_tools.unit_test
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`UnitTest <grading_tools.unit_test.UnitTest>`
  - ```{autodoc2-docstring} grading_tools.unit_test.UnitTest
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`run_pytest <grading_tools.unit_test.run_pytest>`
  - ```{autodoc2-docstring} grading_tools.unit_test.run_pytest
    :summary:
    ```
* - {py:obj}`parse_test_output <grading_tools.unit_test.parse_test_output>`
  - ```{autodoc2-docstring} grading_tools.unit_test.parse_test_output
    :summary:
    ```
````

### API

````{py:function} run_pytest(where: str = './') -> dict[str, UnitTest]
:canonical: grading_tools.unit_test.run_pytest

```{autodoc2-docstring} grading_tools.unit_test.run_pytest
```
````

````{py:function} parse_test_output(log_filename) -> dict[str, UnitTest]
:canonical: grading_tools.unit_test.parse_test_output

```{autodoc2-docstring} grading_tools.unit_test.parse_test_output
```
````

`````{py:class} UnitTest(name: str = '', failed: bool = False, message: str = '', size: int = 1)
:canonical: grading_tools.unit_test.UnitTest

```{autodoc2-docstring} grading_tools.unit_test.UnitTest
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.__init__
```

````{py:method} __bool__() -> bool
:canonical: grading_tools.unit_test.UnitTest.__bool__

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.__bool__
```

````

````{py:method} _combine_messages(connective: str, message1: str, message2: str)
:canonical: grading_tools.unit_test.UnitTest._combine_messages
:staticmethod:

```{autodoc2-docstring} grading_tools.unit_test.UnitTest._combine_messages
```

````

````{py:method} __add__(other: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.__add__

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.__add__
```

````

````{py:method} __mul__(other: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.__mul__

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.__mul__
```

````

````{py:method} __sub__(other: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.__sub__

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.__sub__
```

````

````{py:method} __str__()
:canonical: grading_tools.unit_test.UnitTest.__str__

````

````{py:method} __repr__()
:canonical: grading_tools.unit_test.UnitTest.__repr__

````

````{py:method} either(test1: grading_tools.unit_test.UnitTest, test2: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.either
:staticmethod:

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.either
```

````

````{py:method} both(test1: grading_tools.unit_test.UnitTest, test2: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.both
:staticmethod:

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.both
```

````

````{py:method} unless(test1: grading_tools.unit_test.UnitTest, test2: grading_tools.unit_test.UnitTest) -> grading_tools.unit_test.UnitTest
:canonical: grading_tools.unit_test.UnitTest.unless
:staticmethod:

```{autodoc2-docstring} grading_tools.unit_test.UnitTest.unless
```

````

`````
