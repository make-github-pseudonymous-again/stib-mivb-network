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

A,B = '12'
DESTCODES = [A, B]

ID = 'id'
MODE = 'mode'
LINE = 'line'
DESTCODE = 'destcode'
NAME = 'name'

LATITUDE , LONGITUDE = 'latitude' , 'longitude'

HALT = 'halt'
DESTINATIONS = 'destinations'
FROM = 'destination1'
TO = 'destination2'

TBUS = 'TBUS'
IGNORED = frozenset([ TBUS ])

BBOX = [
  4.267407832744381,
  50.76585836448014,
  4.513419921882967,
  50.92644522461611
]
