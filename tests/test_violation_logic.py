from src.pipeline_types import (
    BoundingBox,
    CrossingEvent,
    TrafficLightState,
)
from src.violation_logic import ViolationDecisionEngine


def make_crossing_event(
    track_id: int,
    light_state: TrafficLightState,
) -> CrossingEvent:
    return CrossingEvent(
        track_id=track_id,
        frame_index=120,
        timestamp_seconds=4.0,
        light_state=light_state,
        bounding_box=BoundingBox(
            x1=100,
            y1=200,
            x2=180,
            y2=300,
        ),
    )


def test_registers_crossing_during_red_as_violation() -> None:
    engine = ViolationDecisionEngine()
    event = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.RED,
    )

    violation = engine.evaluate(event, red_phase_id=1)

    assert violation is not None
    assert violation.track_id == 7
    assert violation.red_phase_id == 1
    assert violation.frame_index == 120


def test_does_not_register_crossing_during_green() -> None:
    engine = ViolationDecisionEngine()
    event = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.GREEN,
    )

    assert engine.evaluate(event, red_phase_id=1) is None


def test_does_not_register_crossing_during_yellow() -> None:
    engine = ViolationDecisionEngine()
    event = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.YELLOW,
    )

    assert engine.evaluate(event, red_phase_id=1) is None


def test_prevents_duplicate_violation_in_same_red_phase() -> None:
    engine = ViolationDecisionEngine()
    event = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.RED,
    )

    first_result = engine.evaluate(event, red_phase_id=1)
    duplicate_result = engine.evaluate(event, red_phase_id=1)

    assert first_result is not None
    assert duplicate_result is None


def test_allows_new_violation_in_later_red_phase() -> None:
    engine = ViolationDecisionEngine()
    event = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.RED,
    )

    first_result = engine.evaluate(event, red_phase_id=1)
    later_phase_result = engine.evaluate(event, red_phase_id=2)

    assert first_result is not None
    assert later_phase_result is not None
    assert later_phase_result.red_phase_id == 2


def test_allows_different_tracks_in_same_red_phase() -> None:
    engine = ViolationDecisionEngine()
    first_car = make_crossing_event(
        track_id=7,
        light_state=TrafficLightState.RED,
    )
    second_car = make_crossing_event(
        track_id=8,
        light_state=TrafficLightState.RED,
    )

    first_result = engine.evaluate(first_car, red_phase_id=1)
    second_result = engine.evaluate(second_car, red_phase_id=1)

    assert first_result is not None
    assert second_result is not None
    assert first_result.track_id != second_result.track_id