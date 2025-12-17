# Programming Students: run this program to see if you have completed the practice question correctly. Remember that
# in pycharm this means you need to select "Current File" in the drop-down box beside the green Run button.

# You don't need to understand or modify this program, it's fairly complicated python :)

# Version 1

import difflib
from io import StringIO
import os
import subprocess
import json
import platform
import inspect
from typing import Callable, Optional
import importlib.util
import sys

linter = "/usr/local/bin/pylint"
if platform.system() == "Windows":
    linter = "I don't know !"
elif platform.system() == "Darwin":  # mac
    linter = "/usr/local/bin/pylint"
elif platform.system() == "Linux":
    linter = "/user/local/bin/pylint"

def lea_file_name_to_days_late(name, due_date,due_month,due_time):
    pass
def modify_and_import(module_name, modification_func):
    """Read in a module, and function that modifies the source code
    and import it.

    EXAMPLE:
    def modify_source(source):
        return source.replace("Foo","FooBar")
    foo = modify_and_import("foo", modify_source)

    # foo.Far() no longer valid
    # foo.FooBar() now works
    """
    spec = importlib.util.find_spec(module_name, None)
    source = spec.loader.get_source(module_name)
    new_source = modification_func(source)
    module = importlib.util.module_from_spec(spec)
    codeobj = compile(new_source, module.__spec__.origin, 'exec')
    exec(codeobj, module.__dict__)
    sys.modules[module_name] = module
    return module


def run_top_level_code_return_output(file, modification_func = lambda x:x):
    module_name = os.path.splitext(file)[0]
    spec = importlib.util.find_spec(module_name, None)
    source = spec.loader.get_source(module_name)
    new_source = modification_func(source)
    module = importlib.util.module_from_spec(spec)
    codeobj = compile(new_source, module.__spec__.origin, 'exec')
    sys.stdin = StringIO()
    sys.stdout = StringIO()
    exec(codeobj, module.__dict__)
    sys.stdout.seek(0)
    output = sys.stdout.readlines()
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    return output




class InputException(Exception):
    """Incorrect calls to input()"""


class CheckException(Exception):
    """Failed checks, like exact-match checks."""


class TopLevelCodeIOException(Exception):
    """There is read/writes in top level code"""


class InputIterator:
    """An iterator for inputs that raises Input errors as appropriate."""

    def __init__(self, data):
        self.data = data
        self.it = iter(data)
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.count += 1
            return next(self.it)
        except StopIteration:
            raise InputException(
                f"Your program asks for input too many times. " +
                f"Please re-read the question, it only asks for {len(self.data)} inputs.")

    def done(self):
        if self.count < len(self.data):
            raise InputException(
                f"Your program asks for input too few times.  Please re-read the question, " +
                f"it asks for {len(self.data)} inputs.")


def how_many_parameters_in_function(foo: Callable) -> int:
    """how many parameters were defined for a given function"""
    params = inspect.signature(foo).parameters
    return len(params)


def explicit_return_in_function(foo: Callable) -> bool:
    import ast
    import inspect
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(foo))))



def import_file(f: str):
    """import the file, checks for errors, checks if io is expected in top-level then just deal with it"""

    # get module name from file name
    name = os.path.splitext(f)[0]

    # allow for io inputs in top-level code (up to 100 inputs)
    sys.stdin = StringIO("1\n" * 100)
    sys.stdout = StringIO()
    module = __import__(name)
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    return module


def run_io(m, f, inputs, func_inputs: Optional[list] = None):
    """Run the function f from the module m with inputs."""
    it = InputIterator(inputs)

    def test_input(s=None):
        # if s is None:
        #     raise Exception(
        #         "Remember that `input()` requires a prompt string.")
        return next(it)

    output = []

    def test_print(*args, **kwargs):
        result = " ".join(map(str, args))
        output.append(result)

    m.input = test_input
    m.print = test_print

    # run code
    if func_inputs is not None:
        f(*func_inputs)
    else:
        f()

    m.input = input
    m.print = print

    it.done()

    return output


def ensure_no_top_level_io(m: str):
    """Ensure there are no top level IO statements in a module."""

    # unload any previous version
    if m in sys.modules:
        del sys.modules[m]

    sys.stdin = StringIO()
    sys.stdout = StringIO()
    try:
        module = __import__(m)
    except EOFError as e:
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        raise TopLevelCodeIOException(
            "You have written code outside of the `main()` function.\n\nRemember that to write all your code "
            "between the line `def main():` and `if __name__ == ...` and each line has to be indented by "
            "at least 4 spaces!\n")

    sys.stdout.seek(0)
    lines = sys.stdout.readlines()
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    if len(lines) != 0:
        raise TopLevelCodeIOException(
            "You have written code outside of the `main()` function.\n\nRemember that to write all your code "
            "between the line `def main():` and `if __name__ == ...` and each line has to be indented by "
            "at least 4 spaces!\n")


def check_match_exact(expected: list[str], actual: list[str], skip_empty_lines: bool = False):
    """Check for an exact match between expected output and actual output. Uses diff to report the differences.
    Raises a CheckException with the difference if there is one."""
    in_expected: list[tuple[int, str]] = []
    in_actual: list[tuple[int, str]] = []

    line_actual: int = 0
    line_expected: int = 0
    for d in difflib.ndiff(expected, actual,
                           linejunk=lambda l: l.strip() == "" if skip_empty_lines else lambda _: False):

        match d[0:2]:
            case "  ":
                line_expected += 1
                line_actual += 1

            case "- ":
                line_expected += 1
                in_expected.append((line_expected, d[2:]))

            case "+ ":
                line_actual += 1
                in_actual.append((line_actual, d[2:]))

            case "? ":
                pass

    if len(in_actual) == 0 and len(in_expected) == 0:
        return

    in_actual_text = "\n".join(map(lambda t: f"{t[0]:>4}| {t[1]}", in_actual))
    in_expected_text = "\n".join(
        map(lambda t: f"{t[0]:>4}| {t[1]}", in_expected))

    if len(in_actual) == 0:
        raise CheckException(
            f"I was expecting more output: \n\nLine\n{in_expected_text}\n")
    if len(in_expected) == 0:
        raise CheckException(
            f"I was expecting less output: \n\nLine\n{in_actual_text}\n")
    raise CheckException(
        f"I was expecting:\n\nLine\n{in_expected_text}\n\nbut you printed:\n\nLine\n{in_actual_text}\n")


def header(label):
    """Print the output header."""
    title = "Checking your solution for " + label
    print()
    print(title)
    print("=" * len(title))


def success():
    """Print the output success message."""
    print("Well done!")


def fails():
    """Print the output failure message."""
    print("Try again :)")


def survey(url):
    """Print the survey prompt with the url."""
    print()
    print("When you're done, click here and let us know " + url)


def check_io(mod, func, inputs, expected, label=None, match_func=check_match_exact):
    """Call the function with these inputs and check for an exact match with expected.
    Prints Pass or Fail message."""
    try:
        output = run_io(mod, func, inputs)
        match_func(expected, output)
        print("✅ Passes" + (f" for {label}." if label is not None else ""))
        return True
    except CheckException as e:
        for line in ("❌ There's a problem with your solution. " + (f"For {label}, " if label is not None else "") + str(
                e)).split("\n"):
            print(line)
        return False


# =============================================================================
# SECTION: Code Quality
# =============================================================================

def errors_and_warnings(files: list[str]) -> tuple[str, str]:
    all_errors = []
    all_warnings = []

    for f in files:
        warning_list, error_list = pylint(f)
        if len(error_list) != 0:
            all_errors.extend(f"{f}: {x}" for x in error_list)
        if len(warning_list) != 0:
            all_warnings.extend(f"{f}: {x}" for x in warning_list)
    str_errors = "<br>".join(all_errors)
    str_warnings = "<br>".join(all_warnings)
    return str_errors, str_warnings


def pylint(file: str) -> tuple[list[str], list[str]]:
    if os.path.exists(linter):

        # pylint file, but have the output in json
        args = [linter, "--output-format=json", file]

        # run the process
        process = subprocess.Popen(args, stdout=subprocess.PIPE)

        # get the output from stdout
        data = process.communicate()[0].decode('utf-8')
        infos: list[dict[str:str]] = json.loads(data)

        # search for output that matches the type of output you are looking for
        errors = []
        warnings = []

        for info in (i for i in infos if i['type'] == "error"):
            errors.append(f"line: {info['line']}: {info['message']}")
        for info in (i for i in infos if i['type'] == "warning"):
            warnings.append(f"line: {info['line']}: {info['message']}")
        return warnings, errors

    else:
        return [], ["Install pylint!!!"]
