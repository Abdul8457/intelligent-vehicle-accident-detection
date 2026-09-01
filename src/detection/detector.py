from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass(frozen=True)
class DetectionConfig:
    acceleration_threshold_g: float = 3.0
    gyro_threshold_dps: float = 180.0
    confirmation_window_samples: int = 3


@dataclass(frozen=True)
class AccidentEvent:
    timestamp: str
    sample_index: int
    peak_acceleration_g: float
    peak_gyro_dps: float


class AccidentDetector:
    """Simple rule-based prototype for accident-event detection."""

    def __init__(self, config: DetectionConfig | None = None):
        self.config = config or DetectionConfig()

    def process_dataframe(self, df: pd.DataFrame) -> List[AccidentEvent]:
        events: List[AccidentEvent] = []
        consecutive = 0
        peak_acc = 0.0
        peak_gyro = 0.0

        for index, row in df.iterrows():
            acceleration = abs(float(row["acceleration_g"]))
            gyro = abs(float(row["gyro_dps"]))
            abnormal = (
                acceleration >= self.config.acceleration_threshold_g
                or gyro >= self.config.gyro_threshold_dps
            )

            if abnormal:
                consecutive += 1
                peak_acc = max(peak_acc, acceleration)
                peak_gyro = max(peak_gyro, gyro)

                if consecutive >= self.config.confirmation_window_samples:
                    events.append(
                        AccidentEvent(
                            timestamp=str(row["timestamp"]),
                            sample_index=int(index),
                            peak_acceleration_g=peak_acc,
                            peak_gyro_dps=peak_gyro,
                        )
                    )
                    consecutive = 0
                    peak_acc = 0.0
                    peak_gyro = 0.0
            else:
                consecutive = 0
                peak_acc = 0.0
                peak_gyro = 0.0

        return events
