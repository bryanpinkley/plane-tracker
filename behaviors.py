import json
import math
import requests
import time

from classes import AirplaneDatabase
from constants import HOME_LAT, HOME_LON


def get_aircraft_positions() -> list:
    """
    Pulls the current aircraft data from the Raspberry Pi. Will only pull if the aircraft has 'lat' and 'lon'

    :return: A list containing aircraft data
    :rtype: List
    """
    try:
        # request = requests.get("http://192.168.1.102:8080/data/aircraft.json", timeout=1)
        # return [aircraft for aircraft in request.json().get("aircraft", []) if "lat" in aircraft and "lon" in aircraft]
        with open("example.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            aircraft
            for aircraft in data.get("aircraft", [])
            if "lat" in aircraft and "lon" in aircraft
        ]
    except:
        return []


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on a sphere, in KM using the haversine formula"""
    # Mean radius of the earth (km)
    R = 6371.0
    # Convert lat and lon to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Find difference between lat and lon
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Calculate the distance
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Create an instance of the in-memory airplane database
db = AirplaneDatabase()

current_planes = db.get_all_planes()

# Call function to pull latest aircraft data
aircraft_list = get_aircraft_positions()

# Store aircraft that is the closest from our home lat/lon
closest_aircraft = {
    "hex": None,
    "min_distance": 0,
}

for aircraft in aircraft_list:
    # Clean data
    hex = aircraft.get("hex", "")
    flight = aircraft.get("flight", "")
    lat = aircraft.get("lat", 0)
    lon = aircraft.get("lon", 0)
    alt = aircraft.get("alt_baro", 0)
    speed = aircraft.get("gs", 0)
    track = aircraft.get("track", 0)

    # If there is no hex, skip plane since that is our unique ID
    if not hex:
        continue

    # See if the plane exists in the database
    if db.exists(hex):
        # If so, update the plane instance
        result = db.update_plane(
            hex, flight=flight, lat=lat, lon=lon, alt=alt, speed=speed, track=track
        )
        # Remove this plane from current_planes so we know we updated it
        del current_planes[hex]
    else:
        # Otherwise, add plane to DB
        result = db.add_plane(hex, flight, lat, lon, alt, speed, track)
    print(result)

    # Determine which plane is the closest
    distance = haversine(HOME_LAT, HOME_LON, lat, lon)
    if closest_aircraft["hex"] is None or distance < closest_aircraft["min_distance"]:
        closest_aircraft["hex"] = hex
        closest_aircraft["min_distance"] = distance

# Need to delete the planes that are in the database but not in the latest json data
for old_plane_hex in current_planes:
    result = db.remove_plane[old_plane_hex]
    print(result)

print("CLOSEST PLANE")
print(closest_aircraft["hex"])
print(round(closest_aircraft["min_distance"], 2), "km")

# print("### TESTING ###")
# print(db.get_all_planes())
# db.remove_plane("aa7e7c")
# print(db.get_all_planes())
# print("### TESTING ###")
# print(db.get_plane_by_hex("ac13f9"))
# print(db.get_plane_by_hex("ac13f9").alt)
# db.update_plane("ac13f9", flight="BP1234", alt=1)
# print(db.get_plane_by_hex("ac13f9"))
# print(db.get_plane_by_hex("ac13f9").alt)
