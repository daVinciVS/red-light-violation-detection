# Real-Time Red-Light Violation Detection

A bachelor thesis project for detecting red-light violations at Indonesian urban intersections using a single fixed camera.

## Overview

This project implements and evaluates a computer-vision pipeline that:

- Detects cars using YOLOv8
- Maintains vehicle identities using ByteTrack
- Estimates traffic-light states using HSV color analysis
- Detects stop-line crossing events using a virtual tripwire
- Flags vehicles that cross the stop line during a red signal phase
- Evaluates detection, tracking, traffic-light classification, violation detection, and processing speed

## Research Context

The system is designed for a single fixed-camera view of the FMIPA UGM intersection on Jalan Sains, Yogyakarta. The camera view includes the vehicle approach lane, stop line, zebra crossing, and relevant traffic-light head.

The project focuses on the `car` class. Motorcycles and other traffic participants may appear in the scene but are outside the main detection scope.

## Proposed Pipeline

```text
Input video
  → Vehicle ROI selection
  → YOLOv8 car detection
  → ByteTrack multi-object tracking
  → HSV traffic-light state estimation
  → Stop-line crossing detection
  → Red-light violation decision
  → Evidence generation and evaluation
```

## Repository Structure

```text
├── configs/        # Model, dataset, ROI, and experiment configuration
├── data/           # Local datasets and metadata; raw data is ignored by Git
├── models/         # Local model weights; ignored by Git
├── notebooks/      # Exploratory analysis and experiment notebooks
├── outputs/        # Generated videos, figures, metrics, and logs; ignored by Git
├── src/            # Source code for the detection pipeline
└── tests/          # Automated tests
```

## Status

Work in progress — dataset organization and baseline implementation.

## Ethical and Privacy Notice

This repository does not contain raw intersection videos, personally identifiable data, license-plate records, or enforcement-ready outputs. The system is developed for academic research and evaluation purposes only.