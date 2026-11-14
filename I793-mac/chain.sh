#!/bin/bash
# run queue 2 after queue 1, and queue 3 after queue 2 (one process at a time)
cd "$(dirname "$0")"
until grep -q " done$" queue1.log; do sleep 15; done
./queue2.sh > queue2.log 2>&1
./queue3.sh > queue3.log 2>&1
