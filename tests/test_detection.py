import pandas as pd
import pytest

from src.detection.detector import (
    AccidentDetector,
    DetectionConfig,
)


def make_df(acceleration, gyro):
    return pd.DataFrame(
        {
            "timestamp": [
                f"t{i}" for i in range(len(acceleration))
            ],
            "acceleration_g": acceleration,
            "gyro_dps": gyro,
        }
    )


def test_normal_driving_has_no_event():
    df = make_df(
        [0.1, 0.2, 0.1, 0.0],
        [5, 8, 4, 6],
    )

    events = AccidentDetector().process_dataframe(df)

    assert events == []


def test_three_consecutive_abnormal_samples_confirm_event():
    df = make_df(
        [0.1, 3.5, 4.0, 3.2, 0.1],
        [5, 190, 210, 200, 5],
    )

    events = AccidentDetector().process_dataframe(df)

    assert len(events) == 1
    assert events[0].sample_index == 3


def test_confirmed_event_contains_peak_values():
    df = make_df(
        [3.2, 4.1, 5.0],
        [190, 230, 260],
    )

    events = AccidentDetector().process_dataframe(df)

    assert len(events) == 1

    event = events[0]

    assert event.peak_acceleration_g == 5.0
    assert event.peak_gyro_dps == 260.0


def test_event_has_severity():
    df = make_df(
        [3.2, 4.1, 5.0],
        [190, 230, 260],
    )

    events = AccidentDetector().process_dataframe(df)

    assert events[0].severity == "HIGH"


def test_event_duration_is_recorded():
    df = make_df(
        [3.2, 4.1, 5.0],
        [190, 230, 260],
    )

    events = AccidentDetector().process_dataframe(df)

    assert events[0].duration_samples == 3


def test_single_abnormal_sample_is_rejected():
    df = make_df(
        [0.1, 4.0, 0.1, 0.1],
        [5, 220, 5, 5],
    )

    events = AccidentDetector().process_dataframe(df)

    assert events == []


def test_custom_thresholds():
    config = DetectionConfig(
        acceleration_threshold_g=2.0,
        gyro_threshold_dps=100.0,
        confirmation_window_samples=2,
    )

    df = make_df(
        [0.1, 2.5, 2.7],
        [5, 110, 120],
    )

    events = AccidentDetector(
        config
    ).process_dataframe(df)

    assert len(events) == 1


def test_missing_required_column_is_rejected():
    df = pd.DataFrame(
        {
            "timestamp": ["t0"],
            "acceleration_g": [4.0],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        AccidentDetector().process_dataframe(df)


def test_empty_dataframe_is_rejected():
    df = pd.DataFrame(
        columns=[
            "timestamp",
            "acceleration_g",
            "gyro_dps",
        ]
    )

    with pytest.raises(ValueError, match="Sensor data is empty"):
        AccidentDetector().process_dataframe(df)


def test_missing_sensor_value_is_rejected():
    df = pd.DataFrame(
        {
            "timestamp": ["t0", "t1"],
            "acceleration_g": [0.1, None],
            "gyro_dps": [5.0, 10.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing values",
    ):
        AccidentDetector().process_dataframe(df)


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError):
        DetectionConfig(
            acceleration_threshold_g=0
        )

    with pytest.raises(ValueError):
        DetectionConfig(
            confirmation_window_samples=0
        )
