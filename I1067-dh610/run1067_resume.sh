#!/bin/bash
# #1067 (dh610): stage 1 resumed after call 1 (the first launch's planted-1e-20 control, inapplicable at max|F| 9.6e-13, killed the healthy run at 20:25:00 UTC five minutes into call 2; its checkpoint after call 1 survives):
# run1067_s1.py with RESUME_CALLS=1 (lowD_dd.py --resume --it_max 2, calls 2 and 3), then stages 2 and 3 (run1067_s23.py) only if stage 1 chose a state
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 9
PY=/home/nathan/Source/venv-i1058/bin/python
RESUME_CALLS=1 $PY -u run1067_s1.py >> run1067_s1.out 2>&1 || { echo "1067 stage 1 (resumed) did not choose a state: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
[ -f run1067_s23.py ] || { echo "1067 run1067_s23.py is missing: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
exec $PY -u run1067_s23.py >> run1067_s23.out 2>&1
