#!/usr/bin/env sh

INTERVAL_SUCCESS="${1:-600}"
INTERVAL_FAIL="${2:-100}"

while true; do
  if sh fetch.sh; then
    sleep "$INTERVAL_SUCCESS"
  else
    sleep "$INTERVAL_FAIL"
  fi
done
