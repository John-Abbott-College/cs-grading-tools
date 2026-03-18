import difflib
from functools import partial
from io import StringIO
import os
import subprocess
import json
import platform
import inspect
from types import ModuleType
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


# ============================================================================
# Exceptions
# ============================================================================


class InputException(Exception):
    """Incorrect calls to input()"""


class CheckException(Exception):
    """Failed checks, like exact-match checks."""


class TopLevelCodeIOException(Exception):
    """There is read/writes in top level code"""


STDERR = list[str]
STDOUT = list[str]


# ============================================================================
# importing files
# ============================================================================
def import_plus(
    file: str, inputs=None, modification_func=lambda x: x
) -> tuple[ModuleType, STDOUT, STDERR, str]:
    """
    From a file name, find the module (standard lookup procedures) and import

    Option to modify the code before compilation

    Option to feed in user inputs via stdin

    :param file: python file to import
    :param inputs: user inputs (script uses `input` function)
    :param modification_func: function that modifies the source code

    Returns: module, stdout, stderr and source code


    EXAMPLE:

    def modify_source(source):
        return source.replace("Foo","FooBar")

    foo, output  = import_plus("foo", [1,2], modify_source)

    # foo.Foo() no longer valid
    # foo.FooBar() now works
    """

    module_name = os.path.splitext(file)[0]

    # unload any previous version
    if module_name in sys.modules:
        del sys.modules[module_name]

    # using import libraries, find the module and get the source code
    spec = importlib.util.find_spec(module_name, None)
    source = spec.loader.get_source(module_name)

    # modify the source code
    new_source = modification_func(source)

    # create a module from the specification
    module = importlib.util.module_from_spec(spec)

    # compile and execute the code (standard procedure when importing a file)
    if inputs is None:
        inputs = []
    sys.stdin = StringIO("\n".join(inputs))
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        code_obj = compile(new_source, module.__spec__.origin, "exec")
        exec(code_obj, module.__dict__)
        a = module.__spec__.origin
        b = module.__dict__
        pass
    except EOFError:
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        raise TopLevelCodeIOException(
            "This file requires more user input than what was expected\n"
        )
    except SyntaxError:
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        raise ImportError("Could not compile code, there was a syntax error")

    # get the text written to stdout/stderr
    sys.stdout.seek(0)
    output = list(map(str.rstrip, sys.stdout.readlines()))
    sys.stderr.seek(0)
    output_err = list(map(str.rstrip, sys.stderr.readlines()))

    # reset i/o
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    # add the module to the list of imported modules
    sys.modules[module_name] = module

    return module, output, output_err, source


def import_file_with_dummy_dummy_inputs(
    f: str,
) -> tuple[ModuleType, STDOUT, STDERR, str]:
    """import the file, checks for errors, checks if io is expected in top-level
    then just deals with it by passing in integers"""
    return import_plus(f, [str(i) for i in range(100)])


def import_file(f: str) -> tuple[ModuleType, STDOUT, STDERR, str]:
    """Ensure there are no top level IO statements in a file."""
    return import_plus(f)


# ============================================================================
# runs a function while supplied inputs to stdin
# ============================================================================
def run_function_with_io(
    m, f, inputs: list[str], func_inputs: Optional[list] = None
) -> list:
    """
    Run the function f from the module m with inputs.
    :param m: module name
    :param f: function name
    :param inputs: list of user supplied inputs
    :param func_inputs: list of arguments to the function

    :return list: Returns any output to stdout
    """

    # override the module's input function
    it = InputIterator(inputs)

    def test_input(s=None):
        return next(it)

    m.input = test_input

    # override the output's output function
    output = []

    def test_print(*args, **kwargs):
        result = " ".join(map(str, args))
        output.append(result)

    m.print = test_print

    # run code
    if func_inputs is not None:
        f(*func_inputs)
    else:
        f()

    # reset the input/output function to their correct value
    m.input = input
    m.print = print

    it.done()

    return output


# ============================================================================
# validating function signatures and returns
# ============================================================================
def how_many_parameters_in_function(foo: Callable) -> int:
    """how many parameters were defined for a given function"""
    params = inspect.signature(foo).parameters
    return len(params)


# ============================================================================
# has an explicit return statement
# ============================================================================
def explicit_return_in_function(foo: Callable) -> bool:
    import ast
    import inspect

    return any(
        isinstance(node, ast.Return)
        for node in ast.walk(ast.parse(inspect.getsource(foo)))
    )


# ============================================================================
# checking list of strings against another list
# ============================================================================
def check_match_exact(
    expected: list[str], actual: list[str], skip_empty_lines: bool = False
) -> str:
    """Check for an exact match between expected output and actual output. Uses diff to report the differences.
    returns the diff string if there are differences."""
    in_expected: list[tuple[int, str]] = []
    in_actual: list[tuple[int, str]] = []

    line_actual: int = 0
    line_expected: int = 0
    if skip_empty_lines:
        expected = list(filter(lambda x: not x.isspace() and x != "", expected))
        actual = list(filter(lambda x: not x.isspace() and x != "", actual))

    for d in difflib.ndiff(
        expected,
        actual,
        linejunk=lambda l: l.strip() == "" if skip_empty_lines else lambda _: False,
    ):
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
        return ""

    in_actual_text = "\n".join(map(lambda t: f"{t[0]:>4}| {t[1]}", in_actual))
    in_expected_text = "\n".join(map(lambda t: f"{t[0]:>4}| {t[1]}", in_expected))

    if len(in_actual) == 0:
        return f"I was expecting more output: \n\nLine\n{in_expected_text}\n"

    if len(in_expected) == 0:
        return f"I was expecting less output: \n\nLine\n{in_actual_text}\n"
    return f"I was expecting:\n\nLine\n{in_expected_text}\n\nbut you printed:\n\nLine\n{in_actual_text}\n"


# =============================================================================
# SECTION: Code Quality
# =============================================================================


def get_linter_info(file) -> list[dict[str:str]]:
    infos = []
    if os.path.exists(linter):
        args = [linter, "--output-format=json", file]

        process = subprocess.Popen(args, stdout=subprocess.PIPE)

        data = process.communicate()
        linter_output = data[0].decode("utf-8")
        infos: list[dict[str:str]] = json.loads(linter_output)

    else:
        raise ValueError("path to pylint does not exist!!!")

    return infos


def errors_and_warnings(
    linter_infos: list[dict[str:str]],
) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []

    for info in (i for i in linter_infos if i["type"] == "error"):
        errors.append(f"{info['path']}: {info['line']}: {info['message']}")
    for info in (i for i in linter_infos if i["type"] == "warning"):
        warnings.append(f"{info['path']}: {info['line']}: {info['message']}")

    return errors, warnings


def _linter_caught_style_mistakes(message_id, linter_info):
    infos = [
        f"{i['path']}: {i['line']}: {i['message']}"
        for i in linter_info
        if i["message-id"] == message_id
    ]

    return infos


style_missing_class_doc_strings = partial(_linter_caught_style_mistakes, "C0115")
style_missing_function_doc_strings = partial(_linter_caught_style_mistakes, "C0116")
style_invalid_naming_style = partial(_linter_caught_style_mistakes, "C0103")
style_defining_new_property_outside_init = partial(
    _linter_caught_style_mistakes, "W0201"
)
style_left_over_unused_variables = partial(_linter_caught_style_mistakes, "W0612")


# ============================================================================
# Useful class for controlling input requests
# ============================================================================
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
                "Your program asks for input too many times. "
                + f"Please re-read the question, it only asks for {len(self.data)} inputs."
            )

    def done(self):
        if self.count < len(self.data):
            raise InputException(
                "Your program asks for input too few times.  Please re-read the question, "
                + f"it asks for {len(self.data)} inputs."
            )
