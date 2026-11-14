#!/bin/bash
# I809 queue 1: the selftest (planted long-edge box), then every count matter/CSS.md 6 quotes, with the new default.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-809/solver/matter
BG=$M/data/css_bg_k1.jsonl
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
run $M/css_count.py selftest
# css_count.py boxes (symmetric about the real axis): D:RE0:RE1:IM[:RFRAC], quoted count in the comment
for spec in 4:0.2:2.5:1.5 4:2.5:5:0.5 10:0.2:4.5:3 40:0.2:5:2.5 20:0.2:6:3 10:0.2:4.5:3:0.6 10:0.2:4.5:2 \
            4:0.2:5:1.2 10:0.2:4.5:2.4 20:0.2:6:2.9; do
  run $M/css_count.py $BG counts.jsonl $spec
done
# quoted: 1, 1, 4, 2, 4, 4, 2; the boxes CSS.md 6 infers to hold exactly two: 2, 2, 2
# css_locate.py boxes (asymmetric), each zero refined at R = 0.6 x_h
run $M/css_locate.py $BG locate.jsonl 4 2.5 5 0.5 1.5
run $M/css_locate.py $BG locate.jsonl 4 2.5 5 -1.5 -0.5
run $M/css_locate.py $BG locate.jsonl 4 0.2 5 1.5 2.5
run $M/css_locate.py $BG locate.jsonl 10 0.2 4.5 0.05 3
run $M/css_locate.py $BG locate.jsonl 20 0.2 6 0.05 3
# quoted: 1 (2.532 + 1.486i, to 2.521 + 1.510i at 0.6), 1 (conjugate), 3, 1 (3.3226 + 2.5045i, runs to 1), 1 (4.8288 + 2.9969i, runs to 1)
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
