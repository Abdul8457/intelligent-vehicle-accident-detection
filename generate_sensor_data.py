from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("data/sample")
RNG = np.random.default_rng(42)


def base_data(samples: int = 300, sample_rate_hz: int = 50) -> pd.DataFrame:
    timestamps = pd.date_range(
        "2026-01-01 12:00:00",
        periods=samples,
        freq=f"{int(1000 / sample_rate_hz)}ms",
    )
    return pd.DataFrame(
        {
            "timestamp": timestamps.astype(str),
            "acceleration_g": RNG.normal(0.0, 0.08, samples),
            "gyro_dps": RNG.normal(0.0, 5.0, samples),
            "latitude": np.full(samples, 49.0069),
            "longitude": np.full(samples, 8.4037),
            "scenario": "normal",
        }
    )


def make_scenarios() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    normal = base_data()
    normal.to_csv(OUTPUT_DIR / "normal_driving.csv", index=False)

    braking = base_data()
    braking.loc[145:150, "acceleration_g"] = [-1.2, -1.5, -1.8, -1.6, -1.4, -1.2]
    braking["scenario"] = "sudden_braking"
    braking.to_csv(OUTPUT_DIR / "sudden_braking.csv", index=False)

    impact = base_data()
    impact.loc[145:149, "acceleration_g"] = [3.2, 4.1, 5.0, 4.2, 3.4]
    impact.loc[145:149, "gyro_dps"] = [190, 230, 260, 220, 185]
    impact["scenario"] = "impact_event"
    impact.to_csv(OUTPUT_DIR / "impact_event.csv", index=False)

    false_trigger = base_data()
    false_trigger.loc[145, "acceleration_g"] = 4.2
    false_trigger.loc[145, "gyro_dps"] = 230
    false_trigger["scenario"] = "false_trigger"
    false_trigger.to_csv(OUTPUT_DIR / "false_trigger.csv", index=False)


if __name__ == "__main__":
    make_scenarios()
    print(f"Generated datasets in {OUTPUT_DIR.resolve()}")
