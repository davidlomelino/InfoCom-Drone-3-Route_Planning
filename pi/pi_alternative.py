import math
import requests
import argparse
import redis

redis_server = redis.Redis(host="localhost", port=6379)

def your_function():
    """
    Hämtar den aktuella drönarens koordinater från Redis.
    """
    longitude = float(redis_server.get("longitude"))
    latitude = float(redis_server.get("latitude"))
    return longitude, latitude

def distance(coord1, coord2):
    """
    Beräknar avståndet mellan två koordinater (longitude, latitude) i meter
    """
    R = 6371000  # Jordens radie i meter
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Returnerar avståndet i meter

def run(current_coords, from_coords, to_coords, SERVER_URL):
    # Rörelse från current_coords till from_coords
    while True:
        current_coords = your_function()
        with requests.Session() as session:
            drone_location = {'longitude': current_coords[0], 'latitude': current_coords[1]}
            session.post(SERVER_URL, json=drone_location)

        # Kontrollera om vi har nått från-adressen
        if distance(current_coords, from_coords) < 10:  # Om vi är inom 10 meter från från-adressen
            print("Drönaren har nått From address.")
            break

    # Rörelse från from_coords till to_coords
    while True:
        current_coords = your_function()
        with requests.Session() as session:
            drone_location = {'longitude': current_coords[0], 'latitude': current_coords[1]}
            session.post(SERVER_URL, json=drone_location)

        # Kontrollera om vi har nått till-adressen
        if distance(current_coords, to_coords) < 10:  # Om vi är inom 10 meter från till-adressen
            print("Drönaren har nått To address.")
            break

if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(f"Current coordinates: {current_coords}")
    print(f"From coordinates: {from_coords}")
    print(f"To coordinates: {to_coords}")

    run(current_coords, from_coords, to_coords, SERVER_URL)
