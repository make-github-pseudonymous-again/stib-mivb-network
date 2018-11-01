import sys
import json
from logger import log
from stib import LINE, DESTCODE, DESTINATIONS, FROM, TO, NAME, MODE, MODES, TRAM, BUS, METRO
from diagnostic import missing_geolocation

data = json.load(sys.stdin)

stops = data["stops"]
lines = data["lines"]
itineraries = data["itineraries"]
waiting = data["waiting"] = { stopid : [ stopid ] for stopid in stops }
modes = data["modes"] = { BUS : { } , METRO : { } , TRAM : { } }

lines["8"][MODE] = TRAM
lines["9"][MODE] = TRAM

for lineid, line in lines.items() :
    for mode in MODES :
        modes[mode][lineid] = MODE in line and mode == line[MODE]

for lineid, line in lines.items():
    line[FROM] = line[FROM].strip()
    line[TO] = line[TO].strip()

missing = missing_geolocation( stops )

for stop in missing :

    candidates = list(filter( lambda x : x[NAME] == stop[NAME] and DESTINATIONS in x , stops.values()))

    matches = [ ]

    for line , _lines in itineraries.items( ) :

        for iti , _stops in _lines.items( ) :

            for _stopID in _stops :

                if _stopID == stop[ID] :

                    matches.append( ( line , iti ) )

    matches = frozenset( matches )

    for candidate in candidates :

        destinations = frozenset( ( destination[LINE] , destination[DESTCODE] ) for destination in candidate[DESTINATIONS] )

        if matches == destinations :

            id = stop[ID]
            waiting[candidate[ID]] = [ id ]
            stop.update(candidate)
            stop[ID] = id

            break

        elif matches.issubset( destinations ) :

            id = stop[ID]
            waiting[candidate[ID]].append( id )
            stop.update(candidate)
            stop[ID] = id
            stop[DESTINATIONS] = [ destination for destination in
                    stop[DESTINATIONS] if ( destination[LINE] ,
                        destination[DESTCODE] ) in matches ]

            break

    else:
        log( stop[ID] , stop[NAME] , matches )
        for candidate in candidates : log( candidate )

json.dump( data , sys.stdout )
