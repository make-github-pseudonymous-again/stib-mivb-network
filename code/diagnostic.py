from logger import log
from stib import LATITUDE, LONGITUDE, DESTINATIONS

def missing_geolocation( stops ) :

    log( "MISSING GEOLOCATION:")

    missing = [
        stop for stop in stops.values()
        if stop[LATITUDE] is None
        or stop[LONGITUDE] is None
    ]
    log( '{}/{}'.format( len( missing ) , len( stops ) ) )

    return missing

def missing_destinations ( stops ) :

    log( "MISSING DESTINATIONS:")

    missing = [ stop for stop in stops.values() if DESTINATIONS not in stop]
    log( '{}/{}'.format( len( missing ) , len( stops ) ) )

    list(map(log,missing))

    return missing

def diagnose ( data ) :

    lines = data["lines"]
    modes = data["modes"]
    itineraries = data["itineraries"]
    stops = data["stops"]

    missing_geolocation( stops )
    missing_destinations( stops )

if __name__ == "__main__" :
    import sys
    import json
    data = json.load(sys.stdin)
    diagnose(data)
