from math import log10 , ceil , floor
from data import get, has
from logger import log
from stib import LATITUDE, LONGITUDE

def scanner ( bbox ) :

    y0 , y1 , ys = bbox[1] , bbox[3] , 0.01
    x0 , x1 , xs = bbox[0] , bbox[2] , 0.01
    y0 = floor( y0 / ys )
    y1 = ceil( y1 / ys )
    x0 = floor( x0 / ys )
    x1 = ceil( x1 / ys )
    T = ( y1 - y0 ) * ( x1 - x0 )

    for _latitude in range( y0 , y1 ) :

        for _longitude in range( x0 , x1 ) :

            log( "{:.2f}%".format( ( ( x1 - x0 ) *  ( _latitude - y0 ) + ( _longitude - x0 ) ) / T * 100 ) )

            latitude , longitude = round( _latitude * ys , -int(floor(log10(ys))) ), round( _longitude * xs , -int(floor(log10(xs))))

            yield get( 'closest' , latitude , longitude )

def creeper ( stops ) :

    notmissing = [
        ( stop[LATITUDE], stop[LONGITUDE] )
        for stop in stops.values()
        if stop[LATITUDE] is not None
        and stop[LONGITUDE] is not None
        and not has( 'closest' , stop[LATITUDE] , stop[LONGITUDE])
    ]

    j = 1
    for latitude , longitude in notmissing :

        log( "{:.2f}%".format( j / len( notmissing ) * 100 ) )
        j += 1

        yield get( 'closest' , latitude , longitude )
