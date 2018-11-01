import os , sys , json , itertools , urllib.request

from xml.etree import ElementTree

from data import cache, fromfile, has, get, DATA

from logger import log

from convert import dict_from_node, dict_from_dicts, list_from_dicts

from metadata import now

from stib import ID, IGNORED, BBOX, MODE, DESTCODES, HALT, DESTINATIONS

from geolocation import scanner, creeper

lines = { }

itineraries = { }

stops = { }

# retrieve all lines
_lines = get( 'lines' )

# build line objects and itineraries
for _line in _lines :

    line = { tag.tag : tag.text for tag in _line }

    id = line[ID]

    if id in IGNORED : continue

    lines[id] = line

    itineraries[id] = { }

    for x in DESTCODES :

        try :

            _itinerary = get( 'itinerary' , id , x )

            _stops = [ { tag.tag : tag.text for tag in _stop } for _stop in _itinerary ]

            itinerary = [ _stop[ID] for _stop in _stops ]

            itineraries[id][x] = itinerary

            for stop in _stops :

                stops[stop[ID]] = stop

        except :
            pass

allfiles = os.listdir( DATA )
closestfiles = filter( lambda x : x.startswith( 'closest' ) , allfiles  )
closestpaths = map( lambda x : DATA + '/' + x , closestfiles )
allclosestops = map( fromfile , closestpaths )

def process ( _closestops ) :

    for _stop in _closestops :

        stop = dict_from_node( _stop )[HALT]
        stop = dict_from_dicts( stop )
        stop[DESTINATIONS] = list_from_dicts( stop[DESTINATIONS] )

        stops.setdefault( stop[ID] , { } ).update( stop )

for _closestops in itertools.chain( allclosestops , scanner( BBOX ) ) :
    process(_closestops)

while True:
    for _closestops in creeper( stops ):
        process(_closestops)
    else:
        break


data = {
    "lines" : lines ,
    "itineraries" : itineraries ,
    "stops" : stops ,
}

data['creation'] = now()

json.dump( data , sys.stdout )
