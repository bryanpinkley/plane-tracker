import time
import requests
import json

from classes import AirplaneDatabase


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


# Create an instance of the in-memory airplane database
db = AirplaneDatabase()

current_planes = db.get_all_planes()

# Call function to pull latest aircraft data
aircraft_list = get_aircraft_positions()

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

# Need to delete the planes that are in the database but not in the latest json data
for old_plane_hex in current_planes:
    result = db.remove_plane[old_plane_hex]
    print(result)

print("### TESTING ###")
print(db.get_all_planes())
db.remove_plane("aa7e7c")
print(db.get_all_planes())
print("### TESTING ###")
print(db.get_plane_by_hex("ac13f9"))
print(db.get_plane_by_hex("ac13f9").alt)
db.update_plane("ac13f9", flight="BP1234", alt=1)
print(db.get_plane_by_hex("ac13f9"))
print(db.get_plane_by_hex("ac13f9").alt)
