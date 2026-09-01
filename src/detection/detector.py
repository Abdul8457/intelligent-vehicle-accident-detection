from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass(frozen=True)
class DetectionConfig:
    """Configuration parameters for the accident detector."""

    acceleration_threshold_g: float = 3.0
    gyro_threshold_dps: float = 180.0
    confirmation_window_samples: int = 3
    cooldown_samples: int = 25

    def __post_init__(self) -> None:
        if self.acceleration_threshold_g <= 0:
            raise ValueError("Acceleration threshold must be positive.")

        if self.gyro_threshold_dps <= 0:
            raise ValueError("Gyroscope threshold must be positive.")

        if self.confirmation_window_samples <= 0:
            raise ValueError(
                "Confirmation window must be greater than zero."
            )

        if self.cooldown_samples < 0:
            raise ValueError("Cooldown samples cannot be negative.")


@dataclass(frozen=True)
class AccidentEvent:
    """Information describing a confirmed accident event."""

    timestamp: str
    sample_index: int
    peak_acceleration_g: float
    peak_gyro_dps: float
    severity: str
    duration_samples: int


class AccidentDetector:
    """
    Rule-based prototype for vehicle accident-event detection.

    The detector identifies abnormal acceleration or gyroscope
    measurements and confirms an event only when the abnormal
    condition persists for a configurable number of samples.
    """

    def __init__(
        self,
        config: DetectionConfig | None = None,
    ) -> None:
        self.config = config or DetectionConfig()

    def process_dataframe(
        self,
        df: pd.DataFrame,
    ) -> List[AccidentEvent]:
        """
        Process a sensor-data DataFrame and return confirmed events.
        """

        self._validate_dataframe(df)

        events: List[AccidentEvent] = []

        consecutive = 0
        peak_acceleration = 0.0
        peak_gyro = 0.0
        event_start_index: int | None = None

        cooldown_remaining = 0

        for index, row in df.iterrows():

            if cooldown_remaining > 0:
                cooldown_remaining -= 1
                continue

            acceleration = abs(float(row["acceleration_g"]))
            gyro = abs(float(row["gyro_dps"]))

            abnormal = (
                acceleration >= self.config.acceleration_threshold_g
                or gyro >= self.config.gyro_threshold_dps
            )

            if abnormal:

                if event_start_index is None:
                    event_start_index = int(index)

                consecutive += 1

                peak_acceleration = max(
                    peak_acceleration,
                    acceleration,
                )

                peak_gyro = max(
                    peak_gyro,
                    gyro,
                )

                if (
                    consecutive
                    >= self.config.confirmation_window_samples
                ):

                    severity = self._calculate_severity(
                        peak_acceleration,
                        peak_gyro,
                    )

                    duration = (
                        int(index) - event_start_index + 1
                    )

                    events.append(
                        AccidentEvent(
                            timestamp=str(row["timestamp"]),
                            sample_index=int(index),
                            peak_acceleration_g=peak_acceleration,
                            peak_gyro_dps=peak_gyro,
                            severity=severity,
                            duration_samples=duration,
                        )
                    )

                    consecutive = 0
                    peak_acceleration = 0.0
                    peak_gyro = 0.0
                    event_start_index = None

                    cooldown_remaining = (
                        self.config.cooldown_samples
                    )

            else:

                consecutive = 0
                peak_acceleration = 0.0
                peak_gyro = 0.0
                event_start_index = None

        return events

    def _validate_dataframe(
        self,
        df: pd.DataFrame,
    ) -> None:
        """Validate the minimum sensor-data requirements."""

        required_columns = {
            "timestamp",
            "acceleration_g",
            "gyro_dps",
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                "Missing required columns: "
                f"{sorted(missing_columns)}"
            )

        if df.empty:
            raise ValueError("Sensor data is empty.")

        sensor_columns = [
            "acceleration_g",
            "gyro_dps",
        ]

        if df[sensor_columns].isnull().any().any():
            raise ValueError(
                "Sensor data contains missing values."
            )

    def _calculate_severity(
        self,
        peak_acceleration_g: float,
        peak_gyro_dps: float,
    ) -> str:
        """
        Classify the detected event using prototype thresholds.

        The thresholds are intended for simulation and development,
        not for real-world crash certification.
        """

        if (
            peak_acceleration_g >= 5.0
            or peak_gyro_dps >= 300.0
        ):
            return "HIGH"

        if (
            peak_acceleration_g >= 4.0
            or peak_gyro_dps >= 240.0
        ):
            return "MEDIUM"

        return "LOW"
