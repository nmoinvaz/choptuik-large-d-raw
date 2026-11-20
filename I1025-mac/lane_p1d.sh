#!/bin/bash
{
# #1025: after the k_c 63 u0 0.02 re-solve, P1-prime-d (p1d_criteria.log) for k_c 55 then k_c 63, then P4 lane B (p4_criteria.log).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
L=2.15,2.20,2.22,2.24,2.26,2.28,2.33
until grep -q 'lane u0r 63 done' $R/lane_u0r63.log; do sleep 30; done
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') p1d_scan.py $*"; RAYON_NUM_THREADS=4 timeout 10800 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/p1d_scan.py "$@" < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve'; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
run $M/data/l1kc55Fh1025.jsonl $M/data/sol_l1kc55Fh1025_D16.0000.npy 16 $L
if [ -f $M/data/sol_l1kc63Fh1025_D16.0000.npy ] && /Users/nathan/venv-314/bin/python -c "import json,sys; r=[json.loads(l) for l in open('$M/data/l1kc63Fh1025.jsonl')][-1]; sys.exit(0 if r['F'] < 1e-8 else 1)"; then
  run $M/data/l1kc63Fh1025.jsonl $M/data/sol_l1kc63Fh1025_D16.0000.npy 16 $L
else
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') k_c 63: no state or F >= 1e-8, no scan (p1d_criteria.log)"
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') P1-prime-d done; P4 lane B"
bash $R/lane_p4.sh $R/p4_list_b.txt > $R/lane_p4b.log 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane p1d done"
exit
}
