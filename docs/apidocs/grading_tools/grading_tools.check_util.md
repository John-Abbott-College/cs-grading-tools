# {py:mod}`grading_tools.check_util`

```{py:module} grading_tools.check_util
```

```{autodoc2-docstring} grading_tools.check_util
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`InputIterator <grading_tools.check_util.InputIterator>`
  - ```{autodoc2-docstring} grading_tools.check_util.InputIterator
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`import_plus <grading_tools.check_util.import_plus>`
  - ```{autodoc2-docstring} grading_tools.check_util.import_plus
    :summary:
    ```
* - {py:obj}`import_file_with_dummy_dummy_inputs <grading_tools.check_util.import_file_with_dummy_dummy_inputs>`
  - ```{autodoc2-docstring} grading_tools.check_util.import_file_with_dummy_dummy_inputs
    :summary:
    ```
* - {py:obj}`import_file <grading_tools.check_util.import_file>`
  - ```{autodoc2-docstring} grading_tools.check_util.import_file
    :summary:
    ```
* - {py:obj}`run_function_with_io <grading_tools.check_util.run_function_with_io>`
  - ```{autodoc2-docstring} grading_tools.check_util.run_function_with_io
    :summary:
    ```
* - {py:obj}`how_many_parameters_in_function <grading_tools.check_util.how_many_parameters_in_function>`
  - ```{autodoc2-docstring} grading_tools.check_util.how_many_parameters_in_function
    :summary:
    ```
* - {py:obj}`explicit_return_in_function <grading_tools.check_util.explicit_return_in_function>`
  - ```{autodoc2-docstring} grading_tools.check_util.explicit_return_in_function
    :summary:
    ```
* - {py:obj}`check_match_exact <grading_tools.check_util.check_match_exact>`
  - ```{autodoc2-docstring} grading_tools.check_util.check_match_exact
    :summary:
    ```
* - {py:obj}`get_linter_info <grading_tools.check_util.get_linter_info>`
  - ```{autodoc2-docstring} grading_tools.check_util.get_linter_info
    :summary:
    ```
* - {py:obj}`errors_and_warnings <grading_tools.check_util.errors_and_warnings>`
  - ```{autodoc2-docstring} grading_tools.check_util.errors_and_warnings
    :summary:
    ```
* - {py:obj}`_linter_caught_style_mistakes <grading_tools.check_util._linter_caught_style_mistakes>`
  - ```{autodoc2-docstring} grading_tools.check_util._linter_caught_style_mistakes
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`linter <grading_tools.check_util.linter>`
  - ```{autodoc2-docstring} grading_tools.check_util.linter
    :summary:
    ```
* - {py:obj}`STDERR <grading_tools.check_util.STDERR>`
  - ```{autodoc2-docstring} grading_tools.check_util.STDERR
    :summary:
    ```
* - {py:obj}`STDOUT <grading_tools.check_util.STDOUT>`
  - ```{autodoc2-docstring} grading_tools.check_util.STDOUT
    :summary:
    ```
* - {py:obj}`style_missing_class_doc_strings <grading_tools.check_util.style_missing_class_doc_strings>`
  - ```{autodoc2-docstring} grading_tools.check_util.style_missing_class_doc_strings
    :summary:
    ```
* - {py:obj}`style_missing_function_doc_strings <grading_tools.check_util.style_missing_function_doc_strings>`
  - ```{autodoc2-docstring} grading_tools.check_util.style_missing_function_doc_strings
    :summary:
    ```
* - {py:obj}`style_invalid_naming_style <grading_tools.check_util.style_invalid_naming_style>`
  - ```{autodoc2-docstring} grading_tools.check_util.style_invalid_naming_style
    :summary:
    ```
* - {py:obj}`style_defining_new_property_outside_init <grading_tools.check_util.style_defining_new_property_outside_init>`
  - ```{autodoc2-docstring} grading_tools.check_util.style_defining_new_property_outside_init
    :summary:
    ```
* - {py:obj}`style_left_over_unused_variables <grading_tools.check_util.style_left_over_unused_variables>`
  - ```{autodoc2-docstring} grading_tools.check_util.style_left_over_unused_variables
    :summary:
    ```
````

### API

````{py:data} linter
:canonical: grading_tools.check_util.linter
:value: >
   '/usr/local/bin/pylint'

```{autodoc2-docstring} grading_tools.check_util.linter
```

````

````{py:exception} InputException()
:canonical: grading_tools.check_util.InputException

Bases: {py:obj}`Exception`

```{autodoc2-docstring} grading_tools.check_util.InputException
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.check_util.InputException.__init__
```

````

````{py:exception} CheckException()
:canonical: grading_tools.check_util.CheckException

Bases: {py:obj}`Exception`

```{autodoc2-docstring} grading_tools.check_util.CheckException
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.check_util.CheckException.__init__
```

````

````{py:exception} TopLevelCodeIOException()
:canonical: grading_tools.check_util.TopLevelCodeIOException

Bases: {py:obj}`Exception`

```{autodoc2-docstring} grading_tools.check_util.TopLevelCodeIOException
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.check_util.TopLevelCodeIOException.__init__
```

````

````{py:data} STDERR
:canonical: grading_tools.check_util.STDERR
:value: >
   None

```{autodoc2-docstring} grading_tools.check_util.STDERR
```

````

````{py:data} STDOUT
:canonical: grading_tools.check_util.STDOUT
:value: >
   None

```{autodoc2-docstring} grading_tools.check_util.STDOUT
```

````

````{py:function} import_plus(file: str, inputs=None, modification_func=lambda x: x) -> tuple[types.ModuleType, grading_tools.check_util.STDOUT, grading_tools.check_util.STDERR, str]
:canonical: grading_tools.check_util.import_plus

```{autodoc2-docstring} grading_tools.check_util.import_plus
```
````

````{py:function} import_file_with_dummy_dummy_inputs(f: str) -> tuple[types.ModuleType, grading_tools.check_util.STDOUT, grading_tools.check_util.STDERR, str]
:canonical: grading_tools.check_util.import_file_with_dummy_dummy_inputs

```{autodoc2-docstring} grading_tools.check_util.import_file_with_dummy_dummy_inputs
```
````

````{py:function} import_file(f: str) -> tuple[types.ModuleType, grading_tools.check_util.STDOUT, grading_tools.check_util.STDERR, str]
:canonical: grading_tools.check_util.import_file

```{autodoc2-docstring} grading_tools.check_util.import_file
```
````

````{py:function} run_function_with_io(m, f, inputs: list[str], func_inputs: typing.Optional[list] = None) -> list
:canonical: grading_tools.check_util.run_function_with_io

```{autodoc2-docstring} grading_tools.check_util.run_function_with_io
```
````

````{py:function} how_many_parameters_in_function(foo: typing.Callable) -> int
:canonical: grading_tools.check_util.how_many_parameters_in_function

```{autodoc2-docstring} grading_tools.check_util.how_many_parameters_in_function
```
````

````{py:function} explicit_return_in_function(foo: typing.Callable) -> bool
:canonical: grading_tools.check_util.explicit_return_in_function

```{autodoc2-docstring} grading_tools.check_util.explicit_return_in_function
```
````

````{py:function} check_match_exact(expected: list[str], actual: list[str], skip_empty_lines: bool = False) -> str
:canonical: grading_tools.check_util.check_match_exact

```{autodoc2-docstring} grading_tools.check_util.check_match_exact
```
````

````{py:function} get_linter_info(file) -> list[dict[str:str]]
:canonical: grading_tools.check_util.get_linter_info

```{autodoc2-docstring} grading_tools.check_util.get_linter_info
```
````

````{py:function} errors_and_warnings(linter_infos: list[dict[str:str]]) -> tuple[list[str], list[str]]
:canonical: grading_tools.check_util.errors_and_warnings

```{autodoc2-docstring} grading_tools.check_util.errors_and_warnings
```
````

````{py:function} _linter_caught_style_mistakes(message_id, linter_info)
:canonical: grading_tools.check_util._linter_caught_style_mistakes

```{autodoc2-docstring} grading_tools.check_util._linter_caught_style_mistakes
```
````

````{py:data} style_missing_class_doc_strings
:canonical: grading_tools.check_util.style_missing_class_doc_strings
:value: >
   'partial(...)'

```{autodoc2-docstring} grading_tools.check_util.style_missing_class_doc_strings
```

````

````{py:data} style_missing_function_doc_strings
:canonical: grading_tools.check_util.style_missing_function_doc_strings
:value: >
   'partial(...)'

```{autodoc2-docstring} grading_tools.check_util.style_missing_function_doc_strings
```

````

````{py:data} style_invalid_naming_style
:canonical: grading_tools.check_util.style_invalid_naming_style
:value: >
   'partial(...)'

```{autodoc2-docstring} grading_tools.check_util.style_invalid_naming_style
```

````

````{py:data} style_defining_new_property_outside_init
:canonical: grading_tools.check_util.style_defining_new_property_outside_init
:value: >
   'partial(...)'

```{autodoc2-docstring} grading_tools.check_util.style_defining_new_property_outside_init
```

````

````{py:data} style_left_over_unused_variables
:canonical: grading_tools.check_util.style_left_over_unused_variables
:value: >
   'partial(...)'

```{autodoc2-docstring} grading_tools.check_util.style_left_over_unused_variables
```

````

`````{py:class} InputIterator(data)
:canonical: grading_tools.check_util.InputIterator

```{autodoc2-docstring} grading_tools.check_util.InputIterator
```

```{rubric} Initialization
```

```{autodoc2-docstring} grading_tools.check_util.InputIterator.__init__
```

````{py:method} __iter__()
:canonical: grading_tools.check_util.InputIterator.__iter__

```{autodoc2-docstring} grading_tools.check_util.InputIterator.__iter__
```

````

````{py:method} __next__()
:canonical: grading_tools.check_util.InputIterator.__next__

```{autodoc2-docstring} grading_tools.check_util.InputIterator.__next__
```

````

````{py:method} done()
:canonical: grading_tools.check_util.InputIterator.done

```{autodoc2-docstring} grading_tools.check_util.InputIterator.done
```

````

`````
