from src.crossing_events import CrossingEventDetector
from src.pipeline_types import BoundingBox, Point, TrafficLightState


def make_box(bottom_center_x: float, bottom_y: float) -> BoundingBox:
    width = 40
    height = 60

    return BoundingBox(
        x1=bottom_center_x - width / 2,
        y1=bottom_y - height,
        x2=bottom_center_x + width / 2,
        y2=bottom_y,
    )


def test_first_observation_does_not_create_crossing_event() -> None:
    detector = CrossingEventDetector(
        line_start=Point(0, 100),
        line_end=Point(300, 100),
    )

    event = detector.update(
        track_id=1,
        bounding_box=make_box(150, 80),
        frame_index=0,
        timestamp_seconds=0.0,
        light_state=TrafficLightState.RED,
    )

    assert event is None


def test_creates_event_when_track_crosses_stop_line() -> None:
    detector = CrossingEventDetector(
        line_start=Point(0, 100),
        line_end=Point(300, 100),
    )

    detector.update(
        track_id=1,
        bounding_box=make_box(150, 90),
        frame_index=0,
        timestamp_seconds=0.0,
        light_state=TrafficLightState.RED,
    )

    event = detector.update(
        track_id=1,
        bounding_box=make_box(150, 110),
        frame_index=1,
        timestamp_seconds=0.04,
        light_state=TrafficLightState.RED,
    )

    assert event is not None
    assert event.track_id == 1
    assert event.frame_index == 1
    assert event.light_state == TrafficLightState.RED


def test_does_not_duplicate_crossing_event_for_same_track() -> None:
    detector = CrossingEventDetector(
        line_start=Point(0, 100),
        line_end=Point(300, 100),
    )

    detector.update(
        track_id=1,
        bounding_box=make_box(150, 90),
        frame_index=0,
        timestamp_seconds=0.0,
        light_state=TrafficLightState.RED,
    )

    first_event = detector.update(
        track_id=1,
        bounding_box=make_box(150, 110),
        frame_index=1,
        timestamp_seconds=0.04,
        light_state=TrafficLightState.RED,
    )

    second_event = detector.update(
        track_id=1,
        bounding_box=make_box(150, 90),
        frame_index=2,
        timestamp_seconds=0.08,
        light_state=TrafficLightState.RED,
    )

    assert first_event is not None
    assert second_event is None


def test_tracks_are_handled_independently() -> None:
    detector = CrossingEventDetector(
        line_start=Point(0, 100),
        line_end=Point(300, 100),
    )

    for track_id in (1, 2):
        detector.update(
            track_id=track_id,
            bounding_box=make_box(150, 90),
            frame_index=0,
            timestamp_seconds=0.0,
            light_state=TrafficLightState.RED,
        )

    first_event = detector.update(
        track_id=1,
        bounding_box=make_box(150, 110),
        frame_index=1,
        timestamp_seconds=0.04,
        light_state=TrafficLightState.RED,
    )
    second_event = detector.update(
        track_id=2,
        bounding_box=make_box(150, 110),
        frame_index=1,
        timestamp_seconds=0.04,
        light_state=TrafficLightState.RED,
    )

    assert first_event is not None
    assert second_event is not None
    assert first_event.track_id != second_event.track_id