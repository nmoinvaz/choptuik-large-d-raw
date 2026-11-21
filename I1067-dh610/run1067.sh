#!/bin/bash
# #1067 (dh610): stage 1 (run1067_s1.py: lowD_dd.py --Ms 512 from B2's M 384 state, the pilot being its first Newton call), then stages 2 and 3 (run1067_s23.py: the fine plan, the series N 12), only if stage 1 chose a state
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 9
PY=/home/nathan/Source/venv-i1058/bin/python
$PY -u run1067_s1.py >> run1067_s1.out 2>&1 || { echo "1067 stage 1 did not choose a state: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
[ -f run1067_s23.py ] || { echo "1067 run1067_s23.py is missing: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
exec $PY -u run1067_s23.py >> run1067_s23.out 2>&1
