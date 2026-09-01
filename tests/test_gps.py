from src.gps.location import GPSLocation


def test_valid_gps_creates_maps_url():
    location = GPSLocation(49.0069, 8.4037)
    assert "49.006900" in location.maps_url()
    assert "8.403700" in location.maps_url()


def test_invalid_gps_reports_unavailable():
    location = GPSLocation(0.0, 0.0, valid=False)
    assert location.maps_url() == "GPS location unavailable"
