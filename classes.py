class Airplane:
    def __init__(
        self,
        hex: str,
        flight: str,
        lat: float,
        lon: float,
        alt: int,
        speed: float,
        track: float,
    ):
        self.hex = hex
        self.flight = flight
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.speed = speed
        self.track = track

    def __str__(self):
        return self.flight


class AirplaneDatabase:
    def __init__(self):
        self.airplane_dict = {}

    def exists(self, hex: str) -> bool:
        """Determine if a given hex code exists in the database"""
        return True if self.airplane_dict.get(hex) else False

    def add_plane(
        self,
        hex: str,
        flight: str,
        lat: float,
        lon: float,
        alt: int,
        speed: float,
        track: float,
    ) -> dict:
        """Add a plane to the database"""
        # First, verify that this plane does not already exist in the dict
        if not self.exists(hex):
            airplane = Airplane(hex, flight, lat, lon, alt, speed, track)
            self.airplane_dict[hex] = airplane
            return {"success": True, "message": f"Added plane ID {hex}"}
        return {"success": False, "message": f"Plane ID {hex} already exists database"}

    def remove_plane(self, hex: str) -> dict:
        """Remove a plane from the database"""
        if self.exists(hex):
            del self.airplane_dict[hex]
            return {"success": True, "message": f"Removed plane ID {hex}"}
        return {
            "success": False,
            "message": f"Plane ID {hex} does not exist in database",
        }

    def update_plane(self, hex: str, **kwargs) -> dict:
        """Update the attributes for an Airplane object"""
        if self.exists(hex):
            airplane = self.airplane_dict[hex]
            for key, value in kwargs.items():
                setattr(airplane, key, value)
            return {"success": True, "message": f"Updated plane ID {hex}"}
        return {
            "success": False,
            "message": f"Plane ID {hex} does not exist in database",
        }

    def get_all_planes(self) -> dict:
        """Fetches all of the planes in the database"""
        return self.airplane_dict.copy()

    def get_plane_by_hex(self, hex: str) -> Airplane:
        if self.exists(hex):
            return self.airplane_dict[hex]
        return None
