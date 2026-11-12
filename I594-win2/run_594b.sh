#!/usr/bin/env bash
# #594(b): #445's unfinished R 0.2 circle around 0.032 + 3.086i (D 61.0264, M 64, kf 23) on the exact determinant of the double-double mode matrix (--ball=320).
# Code: D:/choptuik-i594 detached at main 4b33cc9 (the ball suffix applies to a given --tag), the built modecount_cx copied from D:/choptuik-i573 (the Rust sources are unchanged since 80b5056).
# #445's arguments (hp/modecount_circle.py <state> <circle> --kf=23 --n0=20 --fmax=1e-15 --tag=D61.0264_M64_kf23) plus --ball=320 --threads=9. Cap 6 h, enforced by hand at the hourly check.
R=/d/choptuik-large-d-raw/I594-win2
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
export PYTHONFAULTHANDLER=1
echo "594b start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_594.txt
cd /d/choptuik-i594/hp || exit 9
"$PY" -u modecount_circle.py data/modecount_state_D61.0264_M64_kf23.npz 0.032,3.086,0.2 --kf=23 --n0=20 --fmax=1e-15 --tag=D61.0264_M64_kf23 --ball=320 --threads=9 \
  --data=$R/data --res=$R/data/res.jsonl > $R/run_594b.log 2>&1
echo "594b exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_594.txt
