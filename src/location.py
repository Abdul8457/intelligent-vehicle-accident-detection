from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GPSLocation:
    latitude: float
    longitude: float
    valid: bool = True

    def maps_url(self) -> str:
        if not self.valid:
            return "GPS location unavailable"
        return f"https://maps.google.com/?q={self.latitude:.6f},{self.longitude:.6f}"
