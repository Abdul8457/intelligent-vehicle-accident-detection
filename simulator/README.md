# Simulator

Generates synthetic vehicle sensor data for development and testing.

## Scenarios

The simulator generates seven synthetic scenarios:

- Normal driving
- Hard braking
- Sharp turn
- Pothole
- False trigger
- Minor collision
- Major collision

The scenarios are used to verify that the detector can distinguish
normal or non-accident vehicle motion from potential accident events.

All generated values are synthetic and intended for software development
and academic demonstration only.

## Usage

From the project root:

```bash
python simulator/generate_sensor_data.py
