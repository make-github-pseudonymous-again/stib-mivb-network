import arrow

TZ = 'Europe/Brussels'
FMT = 'YYYY-MM-DDTHH:mm:ssZZ'
now = lambda : arrow.now(TZ).format(FMT)
