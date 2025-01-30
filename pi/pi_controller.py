import math
import requests
import argparse
import time
from sense_hat import SenseHat

#Write you own function that moves the drone from one place to another 
#the function returns the drone's current location while moving
#====================================================================================================
def your_function(): 
    longitude = 13.21008 #home x
    latitude = 55.71106 # home y
    sense.clear()
    return (longitude, latitude)
#====================================================================================================

def travel(xfrom, yfrom, xto, yto):
    travelspeed = 0.0005 
    distance = math.sqrt((xto-xfrom)**2 + (yto-yfrom)**2) #from start to goal with pythagoras 
    
    #(distance/travelspeed = nbrOfSteps)
    #updating current location during travel

    for i in range(1, int(distance/travelspeed) + 1): #rounded to integer
        x = xfrom + (xto-xfrom)/ (distance / travelspeed) * i 
        y = yfrom + (yto-yfrom)/(distance/travelspeed) * i
        
        with requests.Session() as session:
            drone_location = {'longitude': x,'latitude': y}
            resp = session.post(SERVER_URL, json=drone_location)
        time.sleep(0.1)
        
#method2
def run(current_coords, from_coords, to_coords, SERVER_URL):
    travel(current_coords[0], current_coords[1], from_coords[0], from_coords[1])
    travel(from_coords[0], from_coords[1], to_coords[0], to_coords[1])
     
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

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)