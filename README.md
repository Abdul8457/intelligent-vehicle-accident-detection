# Intelligent Vehicle Accident Detection & Emergency Alert System

A portfolio-oriented embedded and Python project for detecting potential vehicle accidents from motion data, validating events, handling GPS location information, generating emergency alerts, and evaluating the detection logic with automated tests.

> **Project status:** Initial portfolio implementation  
> **Note:** This repository is a reconstruction and extension of an earlier academic accident-detection concept. The current implementation is simulation-first so it can be developed and tested without the original hardware.

## Objectives

- Detect abnormal vehicle motion from acceleration and gyroscope data.
- Validate potential accident events to reduce false triggers.
- Process GPS position information.
- Generate emergency-alert messages.
- Log and analyze sensor data.
- Provide automated software tests.
- Keep the architecture modular so hardware interfaces can be added later.

## Architecture

```text
Sensor / Simulated Data
          |
          v
   Signal Processing
          |
          v
   Accident Detector
          |
          v
   Event Validation
       /       \
   Reject     Confirm
                 |
                 v
              GPS
                 |
                 v
          Alert Manager
                 |
          +------+------+
          |             |
       Message       Event Log
          |             |
          +------+------+
                 v
          Python Analysis
```

## Project Structure

```text
intelligent-vehicle-accident-detection/
├── src/
│   ├── detection/
│   ├── gps/
│   ├── alerts/
│   └── data/
├── simulator/
├── tests/
├── analysis/
├── data/
│   └── sample/
├── firmware/
│   └── arduino/
├── docs/
├── figures/
├── requirements.txt
└── README.md
```

## Quick Start

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Generate scenarios:
```bash
python simulator/generate_sensor_data.py
```

Run detection:
```bash
python -m src.main data/sample/impact_event.csv
```

Run analysis:
```bash
python analysis/analyze_sensor_data.py data/sample/impact_event.csv
```

Run tests:
```bash
pytest -q
```

## Detection Approach

The current prototype uses configurable acceleration and gyroscope thresholds together with a confirmation window. A single abnormal sample is not automatically treated as a confirmed accident.

The thresholds are prototype parameters, not claims about real-world crash detection performance. Real deployment would require calibrated sensors, controlled testing, safety analysis, and representative crash data.

## Hardware Extension

The `firmware/arduino/` directory contains an Arduino-oriented reference implementation. Physical GPS/GSM integration can be added through dedicated interfaces without changing the core detection and testing architecture.

## Safety and Privacy

This is a research/portfolio prototype, not a safety-certified emergency system. Do not use it as a real emergency service.

Sample datasets are synthetic. No real emergency-contact information is included.

## License

MIT License. See `LICENSE`.
