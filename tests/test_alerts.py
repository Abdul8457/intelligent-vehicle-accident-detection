from src.alerts.alert_manager import create_alert_message
from src.detection.detector import AccidentEvent
from src.gps.location import GPSLocation


def test_alert_contains_event_and_location():
    event = AccidentEvent(
        "2026-01-01 12:00:00",
        10,
        4.2,
        210.0,
        "medium",
        3,
    )

    location = GPSLocation(49.0069, 8.4037)

    message = create_alert_message(event, location)

    assert "ACCIDENT ALERT" in message
    assert "4.20 g" in message
    assert "210.0 deg/s" in message
    assert "49.006900" in message
