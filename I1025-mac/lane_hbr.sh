#!/bin/bash
{
# #1025 route (c): the hybrid bracket below 1.935 (dd_hybrid_bracket_criteria.log).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') dd_hybrid.py 1.89,1.90,1.91,1.92,1.925,1.93"
RAYON_NUM_THREADS=4 timeout 3600 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/dd_hybrid.py 1.89,1.90,1.91,1.92,1.925,1.93 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'
echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
exit
}
