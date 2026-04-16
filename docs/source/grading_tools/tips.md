# Tips for Testing in python

## Generic

### tests

Create a file with `test_`*`something`* functions.

Only files that start with `test` will be run during the testing phase (unless you specifically call another function)

### `assert`

Inside each function, tests will pass or fail depending on the `assert` function.

`assert` takes two parameters... a boolean, and a string (optional).  

```python 
assert boolean, "string that explains the test"
```

### `fixture` - run when requested

[link to documentation](https://docs.pytest.org/en/stable/explanation/fixtures.html)

You can create methods that setup environments for your test (add the decorator `@pytext.fixture`) which can then be accessed by adding the function names to the arguments to your test.

```python
@pytest.fixture
def sample_set() -> Set[Student]:
    set: Set[Student] = IdSet(10)
    set.add(Student(3, "Milorad Constant"))
    set.add(Student(8, "Zahra Atanasie"))
    set.add(Student(9, "Ananth Sama"))
    return set

def test_add_duplicate(sample_set):
    assert not sample_set.add(Student(3, "Vaast Marc")), \	
    							"ID 3 already exists, should not create new student"
    assert not sample_set.add(Student(8, "Cleena Moana")), \
    							"ID 8 already exists, should not create new student"
    assert not sample_set.add(Student(9, "Ensar Augustinas")), \
    							"ID 9 already exists, should not create new student"

```

### `fixture` - run before every test

```python
test_list = []

@pytest.fixture
def extend_list():
  return [3,4,5,6]

@pytest.fixture(autouse=True)
def clear_list():
  test_list.clear()
  test_list.append(1)
  test_list.append(2)
  
def test_append_to_list():
  # clear_list has been called before this executes
  test_list.append(3)
  test_list.append(4)
  assert len(test_list) == 4
  
def test_extend_to_list(extend_list):
  # clear_list has been called before this executes
	# extend_list was called because it was specified in the parameter list
  test_list.extend(extend_list)
  assert len(test_list) == 6
  
  
```

### Equality of `float`s

In computers, you cannot compare floats and expect it always to work.

Famous example:  `0.3 == 0.1 + 0.2` is false.

So in `pytest`, there is an option to compare *approximately*.  Below is an example where the two float numbers must be equal within an error margin of `0.001`.

```python
assert math.sqrt(2) == pytest.approx(ans_sqrt2, 0.001)
```





## Code Quality

**student_code.py**

```python
def main():
    """main"""

def foo(x:int,y)->float:
    """foo"""

def bar(x,y):pass

type = 12

class Bar:
    """class Bar"""
    def bar(self): pass
    def foo(self): "Bar.foo"

if __name__ == "__main__":
    main()
```

### `docstring`

To check if a docstring is present for all functions:

**test_code**

```python
from inspect import isfunction, isclass
from typing import Optional
import student_code


def has_docstrings(module_or_class, classname="", names: Optional[list[str]] = None) -> list[str]:
    if names is None:
        names = []
    
    # only look at attributes that are not private (not start with "_")
    for name in (n for n in dir(module_or_class) if not n.startswith("_")):
        
        # get the actual attribute instead of the name
        attr = getattr(module_or_class, name)
        
        # ignore variables so only look at classes and functions
        if isfunction(attr) or isclass(attr):
             if attr.__doc__ is None:
                names.append(f"{classname}{name}")
            
            # if it is a class, then look at the contents of the class
            if isclass(attr):
                _ = has_docstrings(attr, classname=f"{classname}.{name}", names=names)
    
    return names


def test_code_quality_docstrings():
    no_docstrings = has_docstrings(student_code)
    if len(no_docstrings):
        assert False, f"These functions do not have docstrings: {no_docstrings}"
    else:
        assert True


```

**output**

```text
============================= test session starts ==============================
collecting ... collected 1 item

delme.py::test_code_quality_docstrings FAILED                            [100%]
delme.py:18 (test_code_quality_docstrings)
def test_code_quality_docstrings():
        no_docstrings = has_docstrings(student_code)
        if len(no_docstrings):
>           assert False, f"These functions do not have docstrings: {no_docstrings}"
E           AssertionError: These functions do not have docstrings: ['Bar.bar', 'bar']
E           assert False

delme.py:22: AssertionError

```

### No errors or warnings

> I would suggest to show warnings, but not necessarily take marks off.

**Requires**: `pylinter`

```python
import os
import subprocess
import json
linter = "/usr/local/bin/pylint"

def pylint(file:str,type:str="error")->list[str]:
    
    if os.path.exists(linter):
        
        # pylint file, but have the output in json
        args = [linter, "--output-format=json",file]

        # run the process
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
				
        # get the ouput from stdout
        data = process.communicate()[0].decode('utf-8')
        infos:list[dict[str:str]] = json.loads(data)

        # search for output that matches the type of output you are looking for
        error_list = []
        for info in (i for i in infos if i['type'] == type):
            error_list.append(f"line: {info['line']}: {info['message']}")
        return error_list
    
    else:
        return ["Install pylint!!!"]

      
def test_no_errors():
    error_list = pylint("student_code.py")
    if len(error_list) != 0:
        assert False, f"You have the following errors: {error_list}"
    assert True
    
def test_no_warnings():
    warnings_list = pylint("student_code.py","warning")
    if len(warnings_list) != 0:
        assert False, f"You have the following warnings: {warnings_list}"
    assert True

```

**Output**

```text
============================= test session starts ==============================
collecting ... collected 2 items

delme.py::test_no_errors PASSED                                          [ 50%]
delme.py::test_no_warnings FAILED                                        [100%]
delme.py:28 (test_no_warnings)
def test_no_warnings():
  warnings_list = pylint("student_code.py","warning")
  if len(warnings_list) != 0:
>   assert False, f"You have the following warnings: {warnings_list}"
E   AssertionError: You have the following warnings: ["line: 10: Redefining built-in 'type'"]
E   assert False

delme.py:32: AssertionError

```

### `type hinting` when defining functions

To validate that the student has used the correct signature for a particular method:

> *unfortunately* it also requires the name of the parameters to be the same, so not the best test

```python
from inspect import signature
def foo_sig(x: int, y: int) -> float: pass

def test_correct_signatures_for_function_foo():
    assert signature(foo_sig) == signature(student_code.foo), \
        "function ~foo~ does not have the correct signature"
```

## Inputs / Outputs

**student_code.py**

```python
def main():
    """main"""
    x = int(input("Enter an integer: "))
    y = int(input("Enter another integer: "))
    print(f"integer division {x//y}")
    print(f"float division {x/y}")


if __name__ == "__main__":
    main()
```



**test_code.py**

```python
import sys
from io import StringIO
import student_code as sc
import re

def run_code(func:Callable[[],None], inputs: list[str]) -> list[str]:
    """run code with required stdin inputs, and return stdout outputs"""
    
    # define stdin as string IO, with each input separted by "\n"
    sys.stdin = StringIO("\n".join(inputs))
    
    # define stdout as a string IO
    sys.stdout = StringIO()
    
    # run code
    func()
    
    # reset the stdout file to the beginning of the file and read all the lines
    sys.stdout.seek(0)
    lines = sys.stdout.readlines()
    
    # reset stdin/stdout to the 'real' stdin/stdout
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    
    # return the output
    return lines

def test_division_returns_both_integer_and_float():
    output = run_code(sc.main, ["17","5"])
    integer_true = False
    float_true = False
    for line in output:
        if "integer" in line:
            integer_true = True
        if "float" in line:
            float_true = True
    assert integer_true and float_true, "Need both integer and float results"

def test_division_integer():
    output = run_code(sc.main, ["17","5"])
    for line in output:
        if "integer" in line:
            # looking for a 3 followed by anything that is not a "." or 
            # another digit
            assert re.search(r'3[^.\d]',line), "Integer division should be 3"

def test_division_float():
    output = run_code(sc.main, ["17","5"])
    for line in output:
        if "float" in line:
            assert "3.4" in line, "Float division should be 3.4"

```

## `matplotlib`

**student code**

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_area_under_curve_with_rectangles(width, x0: float, x1: float, x_data, y_data, title="Hi"):
    """
    Plot a bar chart showing the rectangles, and plot the original function
    :param width: the width of the rectangle
    :param x_data: the middle position of the rectangle
    :param y_data: the value of the function at the middle point of the rectangle
    :return:
    """

    # get the x,y values for plotting the curve
    x = np.arange(x0, x1, 0.1)
    y = list(map(curve, x))

    # plot the rectangles by using a bar chart
    plt.bar(x_data, y_data, width=width, color="lightgreen", edgecolor="black")
    plt.plot(x, y, "-", linewidth="4")
    plt.title(title)
    plt.ylabel("y(x)")
    plt.xlabel("x")
    plt.show()
    
def curve(x):
    return x**2 + 2*x + 3

```



### Avoid plots showing up

For `matplotlib`, the `show` function is used to show the plot on the screen.  To prevent this, just reset the `.show` method to another method.

```python
import matplotlib.pyplot as plt
plt.show = lambda: None
```

### Saving plots instead of showing them

What if you want to save the plots so that you can see them later, but not have them show up on the screen?

```python
import numpy as np
import matplotlib.pyplot as plt
import student_code as sc

def save_plot(*args,**kwargs):
    plt.savefig("filename.png")

plt.show = save_plot

@pytest.fixture(auto)
@pytest.fixture
def x_data():
  return [3,5,7]

@pytest.fixture
def y_data():
  return [9,125,80]

def test_plotting(x_data, y_data):
    sc.plot_area_under_curve_with_rectangles(2,0,10,x_data,y_data)
    assert True, "managed to plot without crashing.  Yay!"

```

### Checking what was plotted

To ensure that the graph does not have mutliple things written on it, it should always be cleared at the beginning of a test.

`gca` refers to *get current axes*

```python
@pytest.fixture(autouse=True)
def clear_matplotlib_axes():
    axes = plt.gca()
    axes.clear()

```

**fixtures etc**

```python
import numpy as np
import matplotlib.pyplot as plt
import pytest

import student_code as sc

plt.show = lambda:None

@pytest.fixture(autouse=True)
def clear_matplotlib_axes():
    axes = plt.gca()
    axes.clear()

@pytest.fixture
def x_data():
  return [3,5,7]

@pytest.fixture
def y_data():
  return [9,125,80]

@pytest.fixture
def plot_graph(x_data, y_data, clear_matplotlib_axes):
  sc.plot_area_under_curve_with_rectangles(2,0,10,x_data,y_data)
  

def test_plotting(plot_graph):
    assert True, "managed to plot without crashing.  Yay!"

```



**bar chart info**

To get info about what was plotted via a bar chart:

```python
@pytest.fixture
def rectangles(plot_graph):

    # for bar charts, each 'graph' of bars 'bars' are store in axes.containers
    axes = plt.gca()
    bar_containers = axes.containers
    bar_container = bar_containers[0]

    # why each rectangle is stored in a patch is beyond me
    return bar_container.patches

def test_uses_correct_number_of_rectangles(rectangles):
    assert len(rectangles) == 3, f"you should have 3 rectangles, not {len(rectangles)}"

def test_bar_set_correctly(x_data,y_data,rectangles):

    # get the bar chart data for first bar
    r = rectangles[0]
    x1 = r.get_x()
    y2 = r.get_y() + r.get_height()
    x_centre = x1 + 0.5 * r.get_width()

    assert x_centre == x_data[0], "x position is not valid"
    assert y2 == y_data[0], "y position is not valid"

```

**line info**

```python
def test_curve(plot_graph):
    axes = plt.gca()
    line = axes.lines[0]
    x=line.get_xdata()
    y=line.get_ydata()
    midx = x[int(len(x)/2)]
    midy = y[int(len(y)/2)]
    assert midy == sc.curve(midx), "plotted line doesn't match curve"

```
