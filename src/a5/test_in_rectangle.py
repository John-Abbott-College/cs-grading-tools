# checking for two things, detect inside polygon when last line would not be crossed
# when using the specified algorithm
# AND
# checking if student "closed the loop"
import pytest
from my_functions import is_in_polygon


@pytest.fixture
def opening_behind_data():
    return [(0, 0), (5, 5), (9, 6), (10, 2)]


@pytest.fixture
def opening_in_front_data():
    return [(10, 2), (0, 0), (5, 5), (9, 6)]


def test_inside_polygon(opening_behind_data):
    point = (6, 3)
    ans = is_in_polygon(*point, opening_behind_data)
    assert ans == True


def test_to_right_polygon(opening_behind_data):
    point = (1, 1.9)
    ans = is_in_polygon(*point, opening_behind_data)
    assert ans == False


def test_to_left_polygon(opening_behind_data):
    point = (11, 3)
    ans = is_in_polygon(*point, opening_behind_data)
    assert ans == False


def test_above_polygon(opening_behind_data):
    point = (5,5.5)
    ans = is_in_polygon(*point, opening_behind_data)
    assert ans == False


def test_below_polygon(opening_behind_data):
    point = (9.5,10)
    ans = is_in_polygon(*point, opening_behind_data)
    assert ans == False


def test_closed_the_polygon(opening_in_front_data):
    point = (6, 3)
    ans = is_in_polygon(*point, opening_in_front_data)
    assert ans == True
