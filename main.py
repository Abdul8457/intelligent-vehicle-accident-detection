from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.detection.detector import AccidentDetector, DetectionConfig
from src.alerts.alert_manager import create_alert_message
from src.gps.location import GPSLocation


def run(csv_path: str) -> None:
    path = Path(csv_path)
    df = pd.read_csv(path)

    required = {"timestamp", "acceleration_g", "gyro_dps"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    detector = AccidentDetector(DetectionConfig())
    events = detector.process_dataframe(df)

    print(f"Input file: {path}")
    print(f"Samples: {len(df)}")
    print(f"Confirmed accident events: {len(events)}")

    for event in events:
        print(f"\nEvent at {event.timestamp}")
        print(f"Peak acceleration: {event.peak_acceleration_g:.2f} g")
        print(f"Peak gyro: {event.peak_gyro_dps:.1f} deg/s")

        latitude = float(df.iloc[event.sample_index].get("latitude", 49.0069))
        longitude = float(df.iloc[event.sample_index].get("longitude", 8.4037))
        location = GPSLocation(latitude, longitude, valid=True)
        print(create_alert_message(event, location))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run accident detection on CSV sensor data.")
    parser.add_argument("csv_path")
    args = parser.parse_args()
    run(args.csv_path)
