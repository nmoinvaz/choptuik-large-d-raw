#!/bin/bash
# #1058: wait for the build's exit line, then run the checks only if it exited 0.
OUT=/home/nathan/Source/choptuik-large-d-raw/I1058-dh170
until grep -q '^# .* UTC build exit' $OUT/build.log 2>/dev/null; do sleep 30; done
rc=$(grep '^# .* UTC build exit' $OUT/build.log | tail -1 | sed 's/.*build exit \([0-9]*\).*/\1/')
[ "$rc" = 0 ] || { echo "build exit $rc, checks not started"; exit 3; }
sleep 20   # versions.txt is written just after the exit line
echo "build ok at $(date -u '+%F %T'), starting the checks"
bash $OUT/checks1058.sh
