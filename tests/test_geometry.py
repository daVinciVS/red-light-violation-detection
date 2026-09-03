from src.geometry import has_crossed_line
from src.pipeline_types import Point


def test_detects_crossing_of_horizontal_line() -> None:
    line_start = Point(0, 100)
    line_end = Point(200, 100)

    previous_point = Point(100, 90)
    current_point = Point(100, 110)

    assert has_crossed_line(
        previous_point,
        current_point,
        line_start,
        line_end,
    )


def test_does_not_detect_when_staying_on_same_side() -> None:
    line_start = Point(0, 100)
    line_end = Point(200, 100)

    previous_point = Point(80, 80)
    current_point = Point(100, 90)

    assert not has_crossed_line(
        previous_point,
        current_point,
        line_start,
        line_end,
    )