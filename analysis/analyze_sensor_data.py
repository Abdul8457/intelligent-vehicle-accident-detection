from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def analyze(path: str) -> None:
    df = pd.read_csv(path)
    df["sample"] = range(len(df))

    print("Samples:", len(df))
    print("Maximum absolute acceleration:", round(df["acceleration_g"].abs().max(), 3), "g")
    print("Maximum absolute gyro:", round(df["gyro_dps"].abs().max(), 2), "deg/s")

    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df["sample"], df["acceleration_g"])
    plt.axhline(3.0, linestyle="--")
    plt.axhline(-3.0, linestyle="--")
    plt.xlabel("Sample")
    plt.ylabel("Acceleration (g)")
    plt.title("Acceleration Signal")
    plt.tight_layout()
    plt.savefig(output_dir / "acceleration_signal.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["sample"], df["gyro_dps"])
    plt.axhline(180.0, linestyle="--")
    plt.axhline(-180.0, linestyle="--")
    plt.xlabel("Sample")
    plt.ylabel("Gyroscope (deg/s)")
    plt.title("Gyroscope Signal")
    plt.tight_layout()
    plt.savefig(output_dir / "gyroscope_signal.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    args = parser.parse_args()
    analyze(args.csv_path)
