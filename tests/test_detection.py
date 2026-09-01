import pandas as pd

from src.detection.detector import AccidentDetector, DetectionConfig


def make_df(acceleration, gyro):
    return pd.DataFrame({
        "timestamp": [f"t{i}" for i in range(len(acceleration))],
        "acceleration_g": acceleration,
        "gyro_dps": gyro,
    })


def test_normal_driving_has_no_event():
    df = make_df([0.1, 0.2, 0.1, 0.0], [5, 8, 4, 6])
    assert AccidentDetector().process_dataframe(df) == []


def test_three_consecutive_abnormal_samples_confirm_event():
    df = make_df([0.1, 3.5, 4.0, 3.2, 0.1], [5, 190, 210, 200, 5])
    events = AccidentDetector().process_dataframe(df)
    assert len(events) == 1
    assert events[0].sample_index == 3


def test_single_abnormal_sample_is_rejected():
    df = make_df([0.1, 4.0, 0.1, 0.1], [5, 220, 5, 5])
    assert AccidentDetector().process_dataframe(df) == []


def test_custom_thresholds():
    config = DetectionConfig(
        acceleration_threshold_g=2.0,
        gyro_threshold_dps=100.0,
        confirmation_window_samples=2,
    )
    df = make_df([0.1, 2.5, 2.7], [5, 110, 120])
    assert len(AccidentDetector(config).process_dataframe(df)) == 1
