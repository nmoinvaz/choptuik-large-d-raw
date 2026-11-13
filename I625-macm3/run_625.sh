#!/bin/bash
# I625: the sign of the exact det M on the 65-point grid lambda + k*1e-14, k = -32..32 (66 evaluations, k = 0 twice), 4 processes, M 32 (the control,
# centred on the mean of #615's ball lambda(32)) and then M 48 (the mean of its ball lambda(48)). Worktree ~/Source/choptuik-large-d-b596 at main ef466c7.
# Usage: run_625.sh   (waits for #624's last runs, runs the M 32 grid, checks it has exactly one sign change, then the M 48 grid)
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
out=$raw/I625-macm3
while ! grep -q '^M40_s3 exit' $raw/I624-macm3/exits.txt 2>/dev/null || ! grep -q '^M48kf23_s3 exit' $raw/I624-macm3/exits.txt 2>/dev/null; do sleep 20; done
cd /Users/nathan/Source/choptuik-large-d-b596/hp
grid() {  # M
  M=$1
  for p in 0 1 2 3; do
    args=$(awk -v p=$p '(NR - 1) % 4 == p {printf "%s,0 ", $2}' $out/points_M$M.txt)
    start() { (caffeinate -is nice -n 10 python3 -u modecount_qdet.py data/states/up12_D58.0060.npz $args --M=$M --kf=13 --threads=1 --json=$out/qdet_M${M}_p$p.json > $out/qdet_M${M}_p$p.log 2>&1
               echo "M${M}_p$p exit $? at $(date -u +%FT%TZ)" >> $out/exits.txt) & }
    if [ $p = 0 ]; then
      start
      while ! grep -q '^lambda' $out/qdet_M${M}_p0.log 2>/dev/null; do sleep 10; if ! pgrep -f "qdet_M${M}_p0.json" > /dev/null; then break; fi; done   # the state is made and saved by process 0
    else
      start
    fi
  done
  wait
}
grid 32
python3 $out/signs625.py 32 > $out/signs_M32.md
if grep -q '^sign changes 1 ' $out/signs_M32.md; then echo "control passes (M 32 grid has exactly one sign change) at $(date -u +%FT%TZ)" >> $out/exits.txt
else echo "CONTROL FAILED (M 32 grid) at $(date -u +%FT%TZ)" >> $out/exits.txt; exit 1; fi
grid 48
python3 $out/signs625.py 48 > $out/signs_M48.md
echo "M48 grid done at $(date -u +%FT%TZ)" >> $out/exits.txt
