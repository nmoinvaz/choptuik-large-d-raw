#!/bin/bash
# #958: wait for build D to exit, and run the checks only if it exited 0.
OUT=/home/nathan/Source/choptuik-large-d-raw/I958-dh170
until grep -q '^# .* UTC build exit' $OUT/build.log; do sleep 30; done
rc=$(grep '^# .* UTC build exit' $OUT/build.log | tail -1 | sed 's/.*build exit //')
[ "$rc" = 0 ] || { echo "build exit $rc, checks not started"; exit 3; }
sleep 20   # versions_D.txt is written just after the exit line
echo "build ok at $(date -u '+%F %T'), starting the checks"
bash $OUT/checks958.sh
