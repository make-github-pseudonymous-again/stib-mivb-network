
import os , sys , json , itertools , urllib.request

from math import log10 , ceil , floor

from xml.etree import ElementTree

DEBUG = False

URLS = {
    'lines' : 'http://m.stib.be/api/getlinesnew.php',
    'itinerary': 'http://m.stib.be/api/getitinerary.php?line={}&iti={}',
    'waiting' : 'http://m.stib.be/api/getwaitingtimes.php?halt={}',
    'closest' : 'http://m.stib.be/api/getclosestops.php?latitude={}&longitude={}'
}

TESTFILES = {
    'lines' : 'test/lines.xml',
    'itinerary': 'test/itinerary.xml',
    'waiting' : 'test/waitingtimes.xml',
    'closest' : 'test/closestops.xml'
}

BUS , METRO , TRAM = MODES = 'BMT'

A , B = '12'

ID = 'id'
MODE = 'mode'
LINE = 'line'
DESTCODE = 'destcode'
NAME = 'name'

LATITUDE , LONGITUDE = 'latitude' , 'longitude'

HALT = 'halt'
DESTINATIONS = 'destinations'

DATA = 'data'

def log(*args,**kwargs):
    print(*args,**kwargs,file=sys.stderr)

def etd(t):
    return {t.tag : list(map(etd, t)) or t.text}

def ltd(l):
    return { k : v for d in l for k , v in d.items() }

def ltl(l):
    return [ ltd( v ) for d in l for v in d.values( ) ]

def cache ( what , *args ) :

    return DATA + '/' + '_'.join( map( str , [ what , *args ] ) )

def fromfile ( name ) :

    log( 'loading' , name )

    return ElementTree.parse( name ).getroot( )

def has ( what , *args ) :

    if DEBUG : return True

    else :

        _cache = cache( what , *args )

        return os.path.isfile( _cache )

def get ( what , *args ) :

    if DEBUG :

        return fromfile( TESTFILES[what] )

    else :

        _cache = cache( what , *args )

        if not os.path.isfile( _cache ) :

            url = URLS[what].format( *args )

            log( 'downloading' , _cache )

            try :

                ElementTree.parse( urllib.request.urlopen( url ) ).write( _cache )

            except Exception as e :
                log( 'could not retrieve data for' , _cache )
                raise e

        return fromfile( _cache )

_lines = get( 'lines' )

lines = { }

modes = { BUS : { } , METRO : { } , TRAM : { } }

itineraries = { }

stops = { }

for _line in _lines :

    line = { tag.tag : tag.text for tag in _line }

    id = line[ID]

    if id == 'TBUS' : continue

    lines[id] = line

    for mode in MODES :

        modes[mode][id] = MODE in line and mode == line[MODE]

    itineraries[id] = { }

    for x in [ A , B ] :

        try :

            _itinerary = get( 'itinerary' , id , x )

            itinerary = [ { tag.tag : tag.text for tag in _stop } for _stop in _itinerary ]

            itineraries[id][x] = itinerary

            for stop in itinerary :

                stops[stop[ID]] = stop

        except :
            pass

def scanner ( ) :

    y0 , y1 , ys = 50.78 , 50.92 , 0.01
    x0 , x1 , xs = 4.27 , 4.47 , 0.01
    y0 = floor( y0 / ys )
    y1 = ceil( y1 / ys )
    x0 = floor( x0 / ys )
    x1 = ceil( x1 / ys )
    T = ( y1 - y0 ) * ( x1 - x0 )

    for _latitude in range( y0 , y1 ) :

        for _longitude in range( x0 , x1 ) :

            log( "{:.2f}%".format( ( ( x1 - x0 ) *  ( _latitude - y0 ) + ( _longitude
                - x0 ) ) / T * 100 ) )

            latitude , longitude = round( _latitude * ys , -int(floor(log10(ys))) ), round( _longitude * xs , -int(floor(log10(xs))))

            yield get( 'closest' , latitude , longitude )

allfiles = os.listdir( DATA )
closestfiles = filter( lambda x : x.startswith( 'closest' ) , allfiles  )
closestpaths = map( lambda x : DATA + '/' + x , closestfiles )
allclosestops = map( fromfile , closestpaths )

def creeper ( ) :

    notmissing = [ ( i , stop[LATITUDE], stop[LONGITUDE] ) for i , stop in enumerate( stops.values() ) if stop[LATITUDE] is not None and
        stop[LONGITUDE] is not None and not has( 'closest' , stop[LATITUDE] ,
            stop[LONGITUDE])]

    for i , latitude , longitude in notmissing :

        log( "{:.2f}%".format( i / len( notmissing ) * 100 ) )

        yield get( 'closest' , latitude , longitude )

for _closestops in itertools.chain( allclosestops , creeper( ) ) :

    for _stop in _closestops :

        stop = etd( _stop )[HALT]
        stop = ltd( stop )
        stop[DESTINATIONS] = ltl( stop[DESTINATIONS] )

        stops.setdefault( stop[ID] , { } ).update( stop )

log( "MISSING GEOLOCATION:")

missing = [ stop for stop in stops.values() if stop[LATITUDE] is None or
        stop[LONGITUDE] is None ]
log( '{}/{}'.format( len( missing ) , len( stops ) ) )

waiting = { stop : [ stop ] for stop in stops}

for stop in missing :

    candidates = list(filter( lambda x : x[NAME] == stop[NAME] and DESTINATIONS
        in x , stops.values()))

    matches = [ ]

    for line , _lines in itineraries.items( ) :

        for iti , _stops in _lines.items( ) :

            for _stop in _stops :

                if _stop[ID] == stop[ID] :

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

        elif stop[ID] == '7620' :

            # WTF MIVB????
            # line 71 2 = 208 2
            # line 71 1 = 207 2

            id = '7620'
            candidate = stops['4363']

            waiting[candidate[ID]].append( id )
            stop.update(candidate)
            stop[ID] = id
            stop[DESTINATIONS] = [{'name': 'DE BROUCKERE', 'destcode': '2',
                    'line': '71', 'mode': 'B'}]

            break

    else:
        log( stop[ID] , stop[NAME] , matches )
        for candidate in candidates : log( candidate )

log( "MISSING GEOLOCATION:")

missing = [ stop for stop in stops.values() if stop[LATITUDE] is None or
        stop[LONGITUDE] is None ]
log( '{}/{}'.format( len( missing ) , len( stops ) ) )

for line in itineraries :

    for iti in itineraries[line] :

        itineraries[line][iti] = [ stop[ID] for stop in itineraries[line][iti]]

log( "MISSING DESTINATIONS:")

missing = [ stop for stop in stops.values() if DESTINATIONS not in stop]
log( '{}/{}'.format( len( missing ) , len( stops ) ) )

list(map(log,missing))

data = { "lines" : lines , "modes" : modes , "itineraries" : itineraries ,
        "stops" : stops , "waiting" : waiting }

json.dump( data , sys.stdout )

