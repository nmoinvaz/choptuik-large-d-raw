#!/bin/bash
# I770 queue 4: queue 3's locate, stopped at 17:17 (no determinant cache, 4x slower), rerun with the cache on the lower
# half of the strip, 5 < Re < 8, 2.95 < Im < 6.27 (queue 3: the strip winds 1, its upper half 0, at setting A).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
run locate 1 5 8 2.9498939 6.2747878 --set=A,B,C --w=1.7 --out=locate_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
