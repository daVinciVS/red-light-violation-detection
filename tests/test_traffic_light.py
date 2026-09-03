import numpy as np
import pytest
from src.pipeline_types import TrafficLightState
from src.traffic_light import TrafficLightClassifier


@pytest.mark.parametrize(
    ("bgr_color", "expected_state"),
    [
        ((0, 0, 255), TrafficLightState.RED),
        ((0, 255, 255), TrafficLightState.YELLOW),
        ((0, 255, 0), TrafficLightState.GREEN),
    ],
)
def test_classifies_solid_signal_colors(
    bgr_color: tuple[int, int, int],
    expected_state: TrafficLightState,
) -> None:
    classifier = TrafficLightClassifier(
        smoothing_window_frames=1,
        min_signal_pixels=20,
    )
    image = np.full((50, 50, 3), bgr_color, dtype=np.uint8)

    assert classifier.classify(image) == expected_state


def test_returns_unknown_for_dark_image() -> None:
    classifier = TrafficLightClassifier(
        smoothing_window_frames=1,
        min_signal_pixels=20,
    )
    image = np.zeros((50, 50, 3), dtype=np.uint8)

    assert classifier.classify(image) == TrafficLightState.UNKNOWN


def test_smoothing_reduces_single_frame_noise() -> None:
    classifier = TrafficLightClassifier(
        smoothing_window_frames=5,
        min_signal_pixels=20,
    )
    red_image = np.full((50, 50, 3), (0, 0, 255), dtype=np.uint8)
    green_image = np.full((50, 50, 3), (0, 255, 0), dtype=np.uint8)

    for _ in range(4):
        assert classifier.classify(red_image) == TrafficLightState.RED

    assert classifier.classify(green_image) == TrafficLightState.RED