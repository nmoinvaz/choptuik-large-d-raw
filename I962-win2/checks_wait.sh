#!/bin/bash
# waits for the build (build.done) and starts run_checks.sh when it exited 0
OUT=/d/choptuik-i935-raw/I962-win2
while [ ! -e $OUT/build.done ]; do sleep 30; done
if tail -1 $OUT/build.times | grep -q 'exit 0$'; then bash $OUT/run_checks.sh; else echo "build failed, checks not started" > $OUT/checks.done; fi
