from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass

import cv2
import numpy as np

from src.pipeline_types import TrafficLightState


@dataclass(frozen=True)
class HSVRange:
    lower: tuple[int, int, int]
    upper: tuple[int, int, int]


@dataclass(frozen=True)
class TrafficLightMeasurement:
    state: TrafficLightState
    red_pixels: int
    yellow_pixels: int
    green_pixels: int


class TrafficLightClassifier:
    def __init__(
        self,
        smoothing_window_frames: int = 5,
        min_signal_pixels: int = 20,
    ) -> None:
        if smoothing_window_frames < 1:
            raise ValueError("smoothing_window_frames must be at least 1")

        self.min_signal_pixels = min_signal_pixels
        self._state_history: deque[TrafficLightState] = deque(
            maxlen=smoothing_window_frames
        )

        self._red_ranges = (
            HSVRange((0, 100, 70), (10, 255, 255)),
            HSVRange((160, 100, 70), (180, 255, 255)),
        )
        self._yellow_range = HSVRange((15, 100, 70), (35, 255, 255))
        self._green_range = HSVRange((40, 60, 50), (90, 255, 255))

    @staticmethod
    def _pixel_count(hsv_image: np.ndarray, hsv_range: HSVRange) -> int:
        mask = cv2.inRange(
            hsv_image,
            np.array(hsv_range.lower, dtype=np.uint8),
            np.array(hsv_range.upper, dtype=np.uint8),
        )
        return int(cv2.countNonZero(mask))

    def measure(self, roi_bgr: np.ndarray) -> TrafficLightMeasurement:
        if roi_bgr is None or roi_bgr.size == 0:
            raise ValueError("roi_bgr must be a non-empty BGR image")

        hsv_image = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)

        red_pixels = sum(
            self._pixel_count(hsv_image, hsv_range)
            for hsv_range in self._red_ranges
        )
        yellow_pixels = self._pixel_count(hsv_image, self._yellow_range)
        green_pixels = self._pixel_count(hsv_image, self._green_range)

        counts = {
            TrafficLightState.RED: red_pixels,
            TrafficLightState.YELLOW: yellow_pixels,
            TrafficLightState.GREEN: green_pixels,
        }

        state, largest_count = max(counts.items(), key=lambda item: item[1])

        if largest_count < self.min_signal_pixels:
            state = TrafficLightState.UNKNOWN

        return TrafficLightMeasurement(
            state=state,
            red_pixels=red_pixels,
            yellow_pixels=yellow_pixels,
            green_pixels=green_pixels,
        )

    def classify(self, roi_bgr: np.ndarray) -> TrafficLightState:
        raw_state = self.measure(roi_bgr).state
        self._state_history.append(raw_state)

        known_states = [
            state
            for state in self._state_history
            if state != TrafficLightState.UNKNOWN
        ]

        if not known_states:
            return TrafficLightState.UNKNOWN

        return Counter(known_states).most_common(1)[0][0]

    def reset(self) -> None:
        self._state_history.clear()