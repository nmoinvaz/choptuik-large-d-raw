#!/bin/bash
{
# #1025 route (c): cause of the void hionly control (dd_b12_cause_criteria.log).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') dd_b12_cause.py 1.9505,1.955"
RAYON_NUM_THREADS=4 timeout 3600 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/dd_b12_cause.py 1.9505,1.955 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'
echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
exit
}
