from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

OUTPUT_PATH = Path("outputs/evidence_frames/synthetic_traffic_light_demo.png")


def main() -> None:
    canvas = np.zeros((300, 900, 3), dtype=np.uint8)
    canvas[:] = (35, 35, 35)

    samples = [
        ("RED", (0, 0, 255)),
        ("YELLOW", (0, 255, 255)),
        ("GREEN", (0, 255, 0)),
        ("UNKNOWN", (0, 0, 0)),
    ]

    for index, (label, color) in enumerate(samples):
        center_x = 120 + index * 220
        cv2.circle(canvas, (center_x, 130), 55, color, thickness=-1)
        cv2.putText(
            canvas,
            label,
            (center_x - 75, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(OUTPUT_PATH), canvas)

    if not success:
        raise RuntimeError(f"Could not write image to {OUTPUT_PATH}")

    print(f"Created: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()