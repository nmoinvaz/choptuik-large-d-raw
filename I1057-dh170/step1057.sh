#!/bin/bash
# #1057 per new ks_chain3b state (coordinator's order, 2026-11-20): the same steps as #949's step949.sh (tracker, pair fold, row, two-mode fit on the last five states) with stopcheck1057.py for the #1057 stop rule.
# usage: bash step1057.sh      (after a `1057 c3b_... exit 0` line in exits_1057.txt); prints everything the post needs. Writes twomode949_D<D>.log for the newest state.
cd /home/nathan/Source/choptuik-large-d-raw/I1057-dh170 || exit 9
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
$PY -I track949.py > track949.log 2>&1 || { echo "track949 failed"; exit 1; }
$PY -I pairfold949.py > pairfold949_latest.log 2>&1 || { echo "pairfold949 failed"; exit 1; }
$PY -I row949.py 3 | cut -c1-320
D=$($PY -I - <<'PYEOF'
import csv
rows=[r for r in csv.DictReader(open("track949.csv")) if r["chain"]=="4" and r["classified"]=="1"]
print("%.4f"%max(float(r["D"]) for r in rows))
PYEOF
)
$PY -I twomode949.py 5 > twomode949_D$D.log 2>&1; echo "twomode exit $?"; cut -c1-300 twomode949_D$D.log
echo "fold window (five latest states of ks_chain3b):"; grep "(chain 3b)" track949.log | tail -n 3 | cut -c1-200
echo "pair fold:"; tail -n 3 pairfold949_latest.log | cut -c1-200
$PY -I stopcheck1057.py
