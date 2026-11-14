#!/bin/bash
# I809 queue 2: the D = 4 resonance-line box 0.2 < Re < 5, 1.5 < Im < 2.5 counted 4 with the new default (quoted 3).
# Diagnostics: the old start (--K=12) on the same box; the box cut into four in Re, each zero located and refined at
# R = 0.6 x_h; the bottom edge moved from Im 1.5 to 1.52 (a zero near the edge would change the count).
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-809/solver/matter
BG=$M/data/css_bg_k1.jsonl
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
run $M/css_locate.py $BG diag.jsonl 4 0.2 5 1.5 2.5 --K=12
for re in "0.2 1.4" "1.4 2.6" "2.6 3.8" "3.8 5"; do
  run $M/css_locate.py $BG diag.jsonl 4 $re 1.5 2.5
done
run $M/css_locate.py $BG diag.jsonl 4 0.2 5 1.52 2.5
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
