#!/bin/bash
# I1034 win2: step 1 (build), then #1040's step_timing_check (I1040-win2, a few minutes, alone on my side), then step 5 (the bit checks, small), then step 2 (cargo tests); all.done at the end stops the memory watches.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1034-win2
. $OUT/lib1034.sh
log "start run_all.sh"
bash $OUT/run_build.sh
rc=$?
if [ $rc -ne 0 ]; then
  echo "# build exit $rc at $(date -u '+%F %T') UTC: steps 5 and 2 were not run" >> $SUM
else
  bash /d/choptuik-i935-raw/I1040-win2/run_1040.sh
  bash $OUT/run_checks.sh
  bash $OUT/run_cargo.sh
fi
log "run_all.sh end, build exit $rc"
touch $OUT/all.done
exit $rc
