#!/usr/bin/env bash
# #657: #551's box at kf 27 and kf 33 on the exact determinant of the double-double mode matrix (--ball=320, M 48), as run_551.sh ran it at kf 29 and 31: the lambda_phys control (R 0.2) and the four R 0.36 circles,
# K = 27 then 33, 9 threads, from hp/ of the worktree D:/choptuik-i551 at main 98ee71bd with venv-t126's older hpkernel and the modecount_cx copied from D:/choptuik-i573 (the pair #551 used, consistent with each
# other and with #498: the coordinator, 20:15 UTC 12 Nov). The kf K state is made by setup from data/seeds/local/up23_D61.0264.npz. The cache of a ball run ends in _ball320_evals.jsonl.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
HP=/d/choptuik-i551/hp
R=/d/choptuik-large-d-raw/I657-win2
cd "$HP" || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "98ee71bd" ] || { echo "worktree D:/choptuik-i551 is not at 98ee71bd" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
for K in 27 33; do
  mkdir -p $R/kf$K/data
  echo "657 kf$K start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
  t=$(date +%s)
  "$PY" -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 \
     --M=48 --kf=$K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$K --ball=320 --threads=9 --data=$R/kf$K/data > $R/kf$K/run.log 2>&1
  echo "657 kf$K exit $? wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
done
echo "657 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
