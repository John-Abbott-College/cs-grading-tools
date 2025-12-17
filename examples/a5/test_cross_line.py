from my_functions import cross_line


def test_horizontal_line_different_y():
    p1 = (5, 5)
    p2 = (10, 4)
    p3 = (20, 4)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, "Horizontal line needs to return False"


def test_horizontal_line_same_y():
    p1 = (5, 6)
    p2 = (10, 7)
    p3 = (20, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, "Horizontal line needs to return False"


# Vertical ahead
def test_vertical_line_between_ahead_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (10, 4)
    p3 = (10, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_vertical_line_between_ahead_p3y_lt_p2y():
    p1 = (5, 5)
    p3 = (10, 4)
    p2 = (10, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_vertical_line_atop_ahead_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (10, 6)
    p3 = (10, 8)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_atop_ahead_p3y_lt_p2y():
    p1 = (5, 5)
    p2 = (10, 8)
    p3 = (10, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_under_ahead_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (10, 3)
    p3 = (10, 4)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


# Vertical Behind
def test_vertical_line_between_behind_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (4, 4)
    p3 = (4, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_between_behind_p3y_lt_p2y():
    p1 = (5, 5)
    p3 = (4, 4)
    p2 = (4, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_atop_behind_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (4, 6)
    p3 = (4, 8)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_atop_behind_p3y_lt_p2y():
    p1 = (5, 5)
    p2 = (4, 8)
    p3 = (4, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_vertical_line_under_behind_p2y_lt_p3y():
    p1 = (5, 5)
    p2 = (4, 3)
    p3 = (4, 4)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


# not horizontal or not vertical
def test_other_1a():
    p1 = (5, 5)
    p2 = (6, 4)
    p3 = (8, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_other_1b():
    p1 = (5, 5)
    p3 = (6, 4)
    p2 = (8, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_other_2a():
    p1 = (5, 5)
    p2 = (4, 4)
    p3 = (10, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_other_2b():
    p1 = (5, 5)
    p3 = (4, 4)
    p2 = (10, 6)
    answer = cross_line(*p1, *p2, *p3)
    assert answer, f"Point {p1} should cross {p2} {p3}"


def test_other_3a():
    p1 = (5, 5)
    p2 = (4, 5)
    p3 = (6, 5)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_3b():
    p1 = (5, 5)
    p3 = (4, 5)
    p2 = (6, 5)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_4a():
    p1 = (5, 5)
    p2 = (6, 6)
    p3 = (7, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_4b():
    p1 = (5, 5)
    p3 = (6, 6)
    p2 = (7, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_5a():
    p1 = (5, 5)
    p2 = (3, 3)
    p3 = (4, 4)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_5b():
    p1 = (5, 5)
    p3 = (3, 3)
    p2 = (4, 4)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_6a():
    p1 = (5, 5)
    p2 = (7, 6)
    p3 = (4, 5)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_6b():
    p1 = (5, 5)
    p3 = (7, 6)
    p2 = (4, 5)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_7a():
    p1 = (5, 5)
    p2 = (7, 6)
    p3 = (8, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"


def test_other_7b():
    p1 = (5, 5)
    p3 = (7, 6)
    p2 = (8, 7)
    answer = cross_line(*p1, *p2, *p3)
    assert not answer, f"Point {p1} should not cross {p2} {p3}"
