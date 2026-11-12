#!/usr/bin/env bash
# #551: #498's stage-1 box at kf 29 and kf 31 on D 61.0264, M 48, on the exact determinant of the double-double mode matrix (--ball=320): the lambda_phys control (R 0.2) and four R 0.36 circles.
# The command is the coordinator's (comment of 20:10 UTC on #551), K = 29 then 31, 9 threads, from hp/ of the worktree D:/choptuik-i551 at main 98ee71bd. The kf K state is made by setup from the seed
# data/seeds/local/up23_D61.0264.npz (about 13 min). The cache of a ball run ends in _ball320_evals.jsonl (checked below).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
HP=/d/choptuik-i551/hp
R=/d/choptuik-large-d-raw/I551-win2
cd "$HP" || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "98ee71bd" ] || { echo "worktree D:/choptuik-i551 is not at 98ee71bd" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
for K in 29 31; do
  mkdir -p $R/kf$K/data
  echo "551 kf$K start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_551.txt
  t=$(date +%s)
  "$PY" -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 \
     --M=48 --kf=$K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$K --ball=320 --threads=9 --data=$R/kf$K/data > $R/kf$K/run.log 2>&1
  echo "551 kf$K exit $? wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_551.txt
done
echo "551 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_551.txt
