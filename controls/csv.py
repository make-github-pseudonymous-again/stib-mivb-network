#!/usr/bin/env python3

import os
import sys
import json

def entry ( item ) :

    key = item["id"]
    value = (item["time"], item["line_number"], item["line"], item["stop"], item["author"])

    return key, value

def main ( controlsdir ) :

    db = {}

    filenames = os.listdir(controlsdir)

    total = len(filenames)

    for i, filename in enumerate(filenames, 1):

        print('{}/{}'.format(i, total), file=sys.stderr)

        with open(os.path.join(controlsdir,filename)) as fd:
            items = json.load(fd)

        for item in items:
            key, value = entry(item)
            db[key] = value

    for item in sorted(db.values()):
        print(','.join(item))


if __name__ == '__main__' :
    main(sys.argv[1])
