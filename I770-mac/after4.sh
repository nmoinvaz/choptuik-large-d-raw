#!/bin/bash
# start queue 5 when queue 4 has ended
cd "$(dirname "$0")"
until grep -q " done$" queue4.log; do sleep 10; done
./queue5.sh > queue5.log 2>&1
