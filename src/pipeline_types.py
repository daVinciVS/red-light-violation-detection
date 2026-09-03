from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TrafficLightState(str, Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def bottom_center(self) -> Point:
        return Point(
            x=(self.x1 + self.x2) / 2,
            y=self.y2,
        )


@dataclass(frozen=True)
class CrossingEvent:
    track_id: int
    frame_index: int
    timestamp_seconds: float
    light_state: TrafficLightState
    bounding_box: BoundingBox


@dataclass(frozen=True)
class ViolationEvent:
    track_id: int
    frame_index: int
    timestamp_seconds: float
    red_phase_id: int
    bounding_box: BoundingBox