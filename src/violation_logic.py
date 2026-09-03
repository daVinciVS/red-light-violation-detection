from __future__ import annotations

from src.pipeline_types import CrossingEvent, TrafficLightState, ViolationEvent


class ViolationDecisionEngine:
    def __init__(self) -> None:
        self._reported_pairs: set[tuple[int, int]] = set()

    def evaluate(
        self,
        crossing_event: CrossingEvent,
        red_phase_id: int,
    ) -> ViolationEvent | None:
        if crossing_event.light_state != TrafficLightState.RED:
            return None

        event_key = (crossing_event.track_id, red_phase_id)

        if event_key in self._reported_pairs:
            return None

        self._reported_pairs.add(event_key)

        return ViolationEvent(
            track_id=crossing_event.track_id,
            frame_index=crossing_event.frame_index,
            timestamp_seconds=crossing_event.timestamp_seconds,
            red_phase_id=red_phase_id,
            bounding_box=crossing_event.bounding_box,
        )

    def reset(self) -> None:
        self._reported_pairs.clear()