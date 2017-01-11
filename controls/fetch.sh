#!/usr/bin/env sh

DIR_DATA='./data'
DIR_CONTROLS="$DIR_DATA"'/controls'
DIR_LINES="$DIR_DATA"'/lines'

URL_CONTROLS='http://54.229.32.209:8090/controls'
URL_LINES='http://54.229.32.209:8090/lines'

timestamp="$(date '+%s')"

OUT_CONTROLS="$DIR_CONTROLS/$timestamp"
OUT_LINES="$DIR_LINES/$timestamp"

curl "$URL_CONTROLS" > "$OUT_CONTROLS"
curl "$URL_LINES" > "$OUT_LINES"
