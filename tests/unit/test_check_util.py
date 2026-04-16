from pathlib import Path

from jac_cs_grading_tools import check_util

from types import ModuleType

import pytest


# TODO: determine where to store test file strings
# Options:
#   - per-test
#   - fixture files
# Considerations:
#   - discoverability, shareability, documentability
@pytest.fixture
def file_under_test(importable_python_file: Path):
    content = """
def foo(a,b,c):
    pass
    """
    importable_python_file.write_text(content, encoding="utf-8")
    return importable_python_file


# TODO: actual requirements testing instead of just testing that the function call works
def test_import_plus(importable_python_file: Path):
    content = """
def foo(a,b,c):
    pass
    """
    importable_python_file.write_text(content, encoding="utf-8")
    module, stdout, stderr, source = check_util.import_plus(str(importable_python_file))
    assert module.foo
    assert len(stderr) == 0
    assert source == content
    assert True


def test_import_file_with_dummy_dummy_inputs():
    assert True


def test_import_file():
    assert True


def test_ensure_no_top_level_io():
    assert True


def test_run_function_with_io():
    assert True


def test_how_many_parameters_in_function():
    assert True


def test_explicit_return_in_function():
    assert True


def test_contains_func():
    assert True


def test_check_match_exact():
    assert True


def test_get_linter_info():
    assert True


def test_errors_and_warnings():
    assert True
