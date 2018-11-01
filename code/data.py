import os
import urllib.request

import arrow
from xml.etree import ElementTree

from logger import log
from stib import URLS, TESTFILES

DATA = 'data'

DEBUG = False

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

                with urllib.request.urlopen( url ) as connection:
                    ElementTree.parse( connection ).write( _cache )


            except Exception as e :
                log( 'could not retrieve data for' , _cache , ', skipping' )
                return []

        return fromfile( _cache )
