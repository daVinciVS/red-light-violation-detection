from __future__ import annotations

from src.pipeline_types import Point


def side_of_line(point: Point, line_start: Point, line_end: Point) -> float:
    return (
        (line_end.x - line_start.x) * (point.y - line_start.y)
        - (line_end.y - line_start.y) * (point.x - line_start.x)
    )


def has_crossed_line(
    previous_point: Point,
    current_point: Point,
    line_start: Point,
    line_end: Point,
) -> bool:
    previous_side = side_of_line(previous_point, line_start, line_end)
    current_side = side_of_line(current_point, line_start, line_end)

    return previous_side != 0 and current_side != 0 and previous_side * current_side < 0