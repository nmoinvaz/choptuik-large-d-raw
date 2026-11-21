#!/bin/bash
# #1058 win2: step 1 (venv, requirements, pip uninstall multidouble, hp/build.sh), then step 2 (the stored-reference checks); all.done at the end stops the memory watches.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1058-win2
. $OUT/lib1058.sh
log "start run_all.sh"
bash $OUT/run_build.sh
rc=$?
if [ $rc -ne 0 ]; then
  echo "# build exit $rc at $(date -u '+%F %T') UTC: step 2 was not run" >> $SUM
else
  bash $OUT/run_checks.sh
fi
log "run_all.sh end, build exit $rc"
touch $OUT/all.done
exit $rc
