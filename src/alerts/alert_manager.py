from __future__ import annotations

from src.detection.detector import AccidentEvent
from src.gps.location import GPSLocation


def create_alert_message(event: AccidentEvent, location: GPSLocation) -> str:
    return (
        "ACCIDENT ALERT\n"
        "Possible vehicle collision detected.\n"
        f"Time: {event.timestamp}\n"
        f"Peak acceleration: {event.peak_acceleration_g:.2f} g\n"
        f"Peak gyro: {event.peak_gyro_dps:.1f} deg/s\n"
        f"Location: {location.maps_url()}"
    )
