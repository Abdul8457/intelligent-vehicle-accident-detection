from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("data/sample")

SAMPLE_RATE_HZ = 50
SAMPLES = 500

BASE_LATITUDE = 49.0069
BASE_LONGITUDE = 8.4037

RNG = np.random.default_rng(42)


def base_data(
    samples: int = SAMPLES,
    sample_rate_hz: int = SAMPLE_RATE_HZ,
) -> pd.DataFrame:
    """Create a baseline vehicle sensor dataset."""

    timestamps = pd.date_range(
        "2026-01-01 12:00:00",
        periods=samples,
        freq=f"{int(1000 / sample_rate_hz)}ms",
    )

    return pd.DataFrame(
        {
            "timestamp": timestamps.astype(str),
            "acceleration_g": RNG.normal(
                0.0,
                0.08,
                samples,
            ),
            "gyro_dps": RNG.normal(
                0.0,
                5.0,
                samples,
            ),
            "latitude": np.full(
                samples,
                BASE_LATITUDE,
            ),
            "longitude": np.full(
                samples,
                BASE_LONGITUDE,
            ),
            "scenario": "normal_driving",
            "accident_expected": False,
        }
    )


def save_scenario(
    df: pd.DataFrame,
    filename: str,
) -> None:
    """Save a generated scenario to the sample-data directory."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = OUTPUT_DIR / filename

    df.to_csv(
        path,
        index=False,
    )

    print(f"Generated: {path}")


def create_normal_driving() -> pd.DataFrame:
    """Normal vehicle operation."""

    df = base_data()

    df["scenario"] = "normal_driving"

    return df


def create_hard_braking() -> pd.DataFrame:
    """Simulate a strong but non-accident braking event."""

    df = base_data()

    start = 180

    braking_signal = [
        -1.2,
        -1.5,
        -1.8,
        -1.6,
        -1.4,
        -1.2,
    ]

    df.loc[
        start : start + len(braking_signal) - 1,
        "acceleration_g",
    ] = braking_signal

    df["scenario"] = "hard_braking"

    return df


def create_sharp_turn() -> pd.DataFrame:
    """Simulate a rapid steering/rotation event."""

    df = base_data()

    start = 220

    gyro_signal = [
        80,
        120,
        150,
        170,
        150,
        120,
        80,
    ]

    df.loc[
        start : start + len(gyro_signal) - 1,
        "gyro_dps",
    ] = gyro_signal

    df["scenario"] = "sharp_turn"

    return df


def create_pothole() -> pd.DataFrame:
    """Simulate a short road-impact event."""

    df = base_data()

    start = 260

    acceleration_signal = [
        2.2,
        -2.5,
        2.6,
        -2.2,
    ]

    df.loc[
        start : start + len(acceleration_signal) - 1,
        "acceleration_g",
    ] = acceleration_signal

    df["scenario"] = "pothole"

    return df


def create_false_trigger() -> pd.DataFrame:
    """Simulate a single abnormal sensor sample."""

    df = base_data()

    start = 300

    df.loc[
        start,
        "acceleration_g",
    ] = 4.2

    df.loc[
        start,
        "gyro_dps",
    ] = 230.0

    df["scenario"] = "false_trigger"

    return df


def create_minor_collision() -> pd.DataFrame:
    """Simulate a moderate collision event."""

    df = base_data()

    start = 330

    acceleration_signal = [
        3.2,
        3.5,
        3.8,
        3.4,
    ]

    gyro_signal = [
        190,
        205,
        220,
        200,
    ]

    df.loc[
        start : start + len(acceleration_signal) - 1,
        "acceleration_g",
    ] = acceleration_signal

    df.loc[
        start : start + len(gyro_signal) - 1,
        "gyro_dps",
    ] = gyro_signal

    df["scenario"] = "minor_collision"
    df["accident_expected"] = True

    return df


def create_major_collision() -> pd.DataFrame:
    """Simulate a severe collision event."""

    df = base_data()

    start = 380

    acceleration_signal = [
        3.5,
        4.2,
        5.0,
        5.8,
        5.2,
        4.5,
        3.8,
    ]

    gyro_signal = [
        190,
        240,
        280,
        330,
        310,
        270,
        210,
    ]

    df.loc[
        start : start + len(acceleration_signal) - 1,
        "acceleration_g",
    ] = acceleration_signal

    df.loc[
        start : start + len(gyro_signal) - 1,
        "gyro_dps",
    ] = gyro_signal

    df["scenario"] = "major_collision"
    df["accident_expected"] = True

    return df


def make_scenarios() -> None:
    """Generate all predefined vehicle scenarios."""

    scenarios = {
        "normal_driving.csv": create_normal_driving(),
        "hard_braking.csv": create_hard_braking(),
        "sharp_turn.csv": create_sharp_turn(),
        "pothole.csv": create_pothole(),
        "false_trigger.csv": create_false_trigger(),
        "minor_collision.csv": create_minor_collision(),
        "major_collision.csv": create_major_collision(),
    }

    for filename, dataframe in scenarios.items():
        save_scenario(
            dataframe,
            filename,
        )

    print("\nScenario generation completed.")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    make_scenarios()
