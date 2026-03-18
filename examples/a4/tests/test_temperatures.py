import pytest

import temperatures as t
from csv_temperature_indices import MAX_TEMP, MIN_TEMP, DATE_TIME
from typing import Callable
import inspect

import csv

test_filename = "mtl_airport_temperature.csv"
oneline_test_filename = "tests/oneline_airport_temperature.csv"
NUMBER_OF_CORRECT_LINES = 7853


def get_func_calls(caller: Callable) -> list[str]:
    nodes = ast.walk(ast.parse(inspect.getsource(caller)))
    func_calls = (call for call in nodes if isinstance(call, ast.Call))
    call_names = [
        call.func.id for call in func_calls if isinstance(call.func, ast.Name)
    ]
    return call_names


# clears the data before every test
@pytest.fixture(autouse=True)
def clear_data():
    t.DATA_COLUMN_YEARS.clear()
    t.DATA_COLUMN_MAX_TEMPS.clear()
    t.DATA_COLUMN_MIN_TEMPS.clear()


@pytest.fixture()
def index_and_temps_for_date():
    # -73.74,45.47,MONTREAL INTL A,7025251,2014-02-14,2014,2,14,,-2.2,,-6.1,,-4.2,,22.2,,0,,0,,12.4,,12.4,,18,,1,,67,
    fh1 = open(test_filename, "r")
    _ = fh1.readline()
    count = 0
    csv_fh1 = csv.reader(fh1)
    for line in csv_fh1:
        if line[MAX_TEMP] != "" and line[MIN_TEMP] != "":
            if line[DATE_TIME] == "2014-02-14":
                return count, float(line[MAX_TEMP]), float(line[MIN_TEMP])
            count += 1
    return 0, 0, 0


def test_read_airport_temperatures_return_type():
    sig = inspect.signature(t.__getattribute__("read_airport_temperatures"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert sig_return is None


def test_read_airport_temperatures_parameter_types():
    sig = inspect.signature(t.__getattribute__("read_airport_temperatures"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert len(sig_parameters) == 1
    assert sig_parameters["filename"].annotation is str


def test_get_list_of_unique_years_return_type():
    sig = inspect.signature(t.__getattribute__("get_list_of_unique_years"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert sig_return in [list[int], list[float]]


def test_get_list_of_unique_years_parameter_types():
    sig = inspect.signature(t.__getattribute__("get_list_of_unique_years"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert len(sig_parameters) == 0


def test_get_extreme_temperature_count_return_type():
    sig = inspect.signature(t.__getattribute__("get_extreme_temperature_count"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert sig_return is int


def test_get_extreme_temperature_count_parameter_types():
    sig = inspect.signature(t.__getattribute__("get_extreme_temperature_count"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert len(sig_parameters) == 3
    assert sig_parameters["this_year"].annotation in [int, float]
    assert sig_parameters["value"].annotation is float
    assert sig_parameters["check_below"].annotation is bool


def test_plot_return_type():
    sig = inspect.signature(t.__getattribute__("plot"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert sig_return is None


def test_plot_parameter_types():
    sig = inspect.signature(t.__getattribute__("plot"))
    sig_parameters = sig.parameters
    sig_return = sig.return_annotation
    assert len(sig_parameters) == 0


def test_read_temperature_file_uses_filename_parameter():
    t.read_airport_temperatures(oneline_test_filename)
    assert len(t.DATA_COLUMN_MAX_TEMPS) == 1
    assert len(t.DATA_COLUMN_MIN_TEMPS) == 1
    assert len(t.DATA_COLUMN_YEARS) == 1


def test_read_temperature_file_lists_same_size():
    t.read_airport_temperatures(test_filename)
    assert len(t.DATA_COLUMN_MIN_TEMPS) == len(t.DATA_COLUMN_YEARS) and len(
        t.DATA_COLUMN_YEARS
    ) == len(t.DATA_COLUMN_MAX_TEMPS)


def test_read_temperature_file_lists_correct_size():
    t.read_airport_temperatures(test_filename)
    assert len(t.DATA_COLUMN_MIN_TEMPS) == NUMBER_OF_CORRECT_LINES


def test_read_temperature_file_correct_data_for_index(index_and_temps_for_date):
    t.read_airport_temperatures(test_filename)
    index, max_temp, min_temp = index_and_temps_for_date
    assert t.DATA_COLUMN_MIN_TEMPS[index] == min_temp
    assert t.DATA_COLUMN_MAX_TEMPS[index] == max_temp


def test_unique_years():
    t.read_airport_temperatures(test_filename)
    z = list(map(int, t.get_list_of_unique_years()))
    assert len(z) == 23
    for y in range(2000, 2023):
        assert y in z


def test_get_extreme_temperature_count_below():
    t.read_airport_temperatures(test_filename)
    n = t.get_extreme_temperature_count(2004, t.LOW_THRESHOLD, True)
    assert n == 17


def test_get_extreme_temperature_count_above():
    t.read_airport_temperatures(test_filename)
    n = t.get_extreme_temperature_count(2004, t.HIGH_THRESHOLD, False)
    assert n == 12


def test_get_extreme_temperature_count_below_no_hard_coding():
    t.read_airport_temperatures(test_filename)
    n = t.get_extreme_temperature_count(2004, t.LOW_THRESHOLD + 10, True)
    assert n == 71


def test_get_extreme_temperature_count_above_no_hard_coding():
    t.read_airport_temperatures(test_filename)
    n = t.get_extreme_temperature_count(2004, t.HIGH_THRESHOLD - 10, False)
    assert 142 <= n <= 144
