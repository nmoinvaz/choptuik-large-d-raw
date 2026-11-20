#!/bin/bash
{
# #1025 P4 (p4_criteria.log). Usage: lane_p4.sh LIST, each line "RECORDS STATE D [--mutate=f64]".
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
while read -r a b c d; do
  [ -z "$a" ] && continue
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') p4_hybrid.py $a $b $c $d"
  RAYON_NUM_THREADS=4 timeout 10800 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/p4_hybrid.py $a $b $c $d < /dev/null 2>&1 | grep --line-buffered -v "Warning\|sl.solve"
  echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
done < "$1"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane p4 $1 done"
exit
}
