from __future__ import annotations

from dataclasses import dataclass

from src.geometry import has_crossed_line
from src.pipeline_types import (
    BoundingBox,
    CrossingEvent,
    Point,
    TrafficLightState,
)


@dataclass
class TrackCrossingState:
    previous_point: Point
    has_crossed: bool = False


class CrossingEventDetector:
    def __init__(
        self,
        line_start: Point,
        line_end: Point,
    ) -> None:
        self.line_start = line_start
        self.line_end = line_end
        self._track_states: dict[int, TrackCrossingState] = {}

    def update(
        self,
        track_id: int,
        bounding_box: BoundingBox,
        frame_index: int,
        timestamp_seconds: float,
        light_state: TrafficLightState,
    ) -> CrossingEvent | None:
        current_point = bounding_box.bottom_center
        track_state = self._track_states.get(track_id)

        if track_state is None:
            self._track_states[track_id] = TrackCrossingState(
                previous_point=current_point,
            )
            return None

        crossed_now = has_crossed_line(
            previous_point=track_state.previous_point,
            current_point=current_point,
            line_start=self.line_start,
            line_end=self.line_end,
        )

        track_state.previous_point = current_point

        if not crossed_now or track_state.has_crossed:
            return None

        track_state.has_crossed = True

        return CrossingEvent(
            track_id=track_id,
            frame_index=frame_index,
            timestamp_seconds=timestamp_seconds,
            light_state=light_state,
            bounding_box=bounding_box,
        )

    def remove_track(self, track_id: int) -> None:
        self._track_states.pop(track_id, None)

    def reset(self) -> None:
        self._track_states.clear()