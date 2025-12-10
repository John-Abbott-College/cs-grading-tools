# Reference: `check_util`

### Import student code in test file

#### <u>`import_file(f: str) -> tuple[ModuleType, STDOUT, STDERR, str]`</u>

Imports a student file with the given filename. Will re-import (so if code has been modified, it will use the new code)

Arguments:

- `filename`

Returns:

- `module` the module (use if you want to modify something in the module, or use a function within the module)

  `x = module.function_name(input)`

- `stdout` anything that was printed to stdout is returned as a list of strings

- `stderr` anything that was printed to stderr is returned as a list of strings

- `source code` the source code (as a single string)

Usages:

```python
module,_,_,_ = import_file("foo")
x = module.this_func(1,2,3)
assert x == 25
```

```python
module, stdout,_,_ = import_file('foo')
assert stdout[0] == "correct output"
```

```python
module, stdout, stderr, source = import_file('foo.py')
assert "try:" not in source, "No try/except code is allowed!"
```

#### <u>`import_file_with_dummy_dummy_inputs(f: str) -> tuple[ModuleType, STDOUT, STDERR, str]`</u>

Imports a student file with the given filename. Will re-import (so if code has been modified, it will use the new code)

<font color="red">_If the code requires up to 100 inputs, (via an `input` statement), it will still import_</font>

Arguments:

- `filename`

Returns:

- `module` the module (use if you want to modify something in the module, or use a function within the module)

  `x = module.function_name(input)`

- `stdout` anything that was printed to stdout is returned as a list of strings

- `stderr` anything that was printed to stderr is returned as a list of strings

- `source code` the source code (as a single string)

Usages:

```python
# student code
x = input("question 1")
y = input("question 2")

def foo(x,y):
    pass
```

```python
# testing
module,_,_,_ = import_file_with_dummy_dummy_inputs("foo.py")
z = module.foo(6,7)
```

#### <u>`import_plus(f: str, inputs=None, modification_func=lambda x: x) -> tuple[ModuleType, STDOUT, STDERR, str]`</u>

Imports a student file with the given filename, allows for specifying the inputs as it is loaded, and allows the tester to modify the source code before it is properly imported

Arguments:

- `filename`
- `inputs` A list of strings which will be _fed_ the `input` commands in the student code
- `modification_func` A function that takes in one parameter (the source code) and returns the modified source code

Returns:

- `module` the module (use if you want to modify something in the module, or use a function within the module)

  `x = module.function_name(input)`

- `stdout` anything that was printed to stdout is returned as a list of strings

- `stderr` anything that was printed to stderr is returned as a list of strings

- `source code` the source code (as a single string)

Usages:

```python
# student code
CONST = 10
# ...
```

```python
# testing
def change_const(source)
 source = source.replace("CONST = 10", "CONST = 20")
module, _,_,_ = import_plus("foo.py",modification_func=change_const)
```

```python
# student code
n = input("Enter name")
print(f"Hello {n}")
```

```python
# testing
module, stdout, _, _ = import_plus("foo.py", inputs=["Sandy"])
assert stdout[0] == "Hello Sandy"
```

### function access from test file

#### <u>`run_function_with_io(m, f, inputs: list[str], func_inputs: Optional[list] = None) -> list:`</u>

Runs a function that requires inputs for the `input` function, and optionally specific arguments to the function

Arguments:

- `m` the module (see `import_file` to get the module)
- `f` the function (example `my_module.foo`)
- `inputs` a list of strings that will be _fed_ to the `input` functions in the module
- `func_input` any arguments that need to be passed to the module directly

Returns:

- `output` a list of strings of anything that was printed to the console

usage:

```python
# bad student file
def foo(a,b):
    x = input("add or subtract")
    if x == "add":
     return a + b
    else:
        return a - b
```

```python
# testing
m, _,_,_ = import("foo.py")
y = run_function_with_io(m, m.foo, ["add"], [1,2])
assert y == 3
```

#### <u>`how_many_parameters_in_function(foo: Callable) -> int`</u>

Returns the number of parameters in the specified function

usage:

```python
# student file
def foo(a,b,c):
    pass
```

```python
# testing
m,_,_,_ = import_file("foo.py")
y = how_many_parameters_in_function(m.foo)
assert y == 3
```

#### <u>`explicit_return_in_function(foo: Callable) -> bool`</u>

returns `True` if there is an explicit `return` in the specified function

usage:

```python
# student file
def foo(a):
    print (a**2)   # NO!!!!
    return a**2   # Yes (phew)
```

```python
# testing
m,_,_,_ = import_file("foo.py")
assert explitit_return_in_function(m.foo)
```

### Code Quality

`pylint` must be installed!

On Windows, I don't know where it will be installed, so you will need to modify the following code in `check_utils.py`

```python
linter = "/usr/local/bin/pylint"
if platform.system() == "Windows":
    linter = "I don't know !"
```

#### <u>`get_linter_info(file) -> list[dict[str:str]]`</u>

returns the output of `pylint`.

#### <u>`errors_and_warnings(linter_infos: list[dict[str:str]]) -> tuple[list[str], list[str]]`</u>

returns two lists, errors and warnings from the results of `pylint`

Usage:

```python
linter_info = get_linter_info("hotel.py")
e,w = errors_and_warnings(linter_info)
```

#### <u>`style_missing_class_doc_strings(linter_infos: list[dict[str:str]]) -> list[str]`</u>

returns a list of public functions that do not have doc-strings

Usage:

```python
linter_info = get_linter_info("hotel.py")
missing_doc_strings = style_missing_class_doc_strings(linter_info)
```

#### <u>`style_invalid_naming_style(linter_infos: list[dict[str:str]]) -> list[str]`</u>

returns a list of naming style infractions

#### <u>`style_defining_new_property_outside_init(linter_infos: list[dict[str:str]]) -> list[str]`</u>

returns a list of any properties of a class that are set _outside_ of the `__init__` function

#### <u>`style_left_over_unused_variables(linter_infos: list[dict[str:str]]) -> list[str]`</u>

returns a list of variables that were not used

### List Matching

#### <u>`check_match_exact(expected: list[str], actual: list[str], skip_empty_lines: bool = False) -> str`</u>

Uses `ndiff` to compare two lists (similar to what you would get if you used `diff` on a linux machine)

