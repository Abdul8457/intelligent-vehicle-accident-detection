# System Architecture

The project follows a modular architecture that separates accident
detection from GPS handling and alert generation.

## Processing Flow

1. Load or generate vehicle sensor data.
2. Read acceleration and gyroscope measurements.
3. Compare sensor values with configurable thresholds.
4. Require multiple consecutive abnormal samples to confirm an event.
5. Track the peak sensor values and duration of the abnormal event.
6. Obtain the GPS location when an event is confirmed.
7. Generate an emergency-alert message.
8. Analyze the sensor data using Python visualization tools.

## Main Modules

- `src/detection/` — Accident detection and event classification
- `src/gps/` — GPS location handling
- `src/alerts/` — Alert-message generation
- `src/data/` — Sensor-data loading utilities
- `simulator/` — Synthetic vehicle-sensor scenarios
- `analysis/` — Sensor-data visualization
- `tests/` — Automated software tests
- `firmware/arduino/` — Arduino reference implementation

The accident detector is independent from GPS and alert generation,
which allows the detection logic to be tested without physical
communication hardware.

## Scope

The implementation is intended for academic and portfolio
demonstration. The simulated sensor data and detection thresholds
should not be interpreted as real-world crash-detection performance.
