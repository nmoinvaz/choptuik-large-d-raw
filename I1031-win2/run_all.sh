#!/bin/bash
# I1031 win2: the build, then the checks; all.done at the end stops the memory watch.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1031-win2
bash $OUT/run_build.sh
rc=$?
if [ $rc -ne 0 ]; then
  echo "# build exit $rc at $(date -u '+%F %T') UTC: the checks were not run" >> $OUT/summary_1031.txt
else
  bash $OUT/run_checks.sh
fi
touch $OUT/all.done
exit $rc
