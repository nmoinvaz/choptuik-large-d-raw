#!/bin/bash
# I995-mac m1b: M = 1 count at xi1 0.17 (zeros again at 0.2), then the planted run on the same cache; code 8e770023
cd /Users/nathan/Source/choptuik-large-d-995/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
OUT=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/c1624759-29b0-41ee-b1ba-c50f07eff81b/scratchpad/raw983/I995-mac/m1b
echo "== start $(date -u '+%F %T')"
gtimeout 6h nice -n 10 $PY -u argcount.py --M=1 --A=0.5,6 --wf=0.2,3 --nA=22 --nwf=28 --procs=2 --out=$OUT --tag=M1_full 2>&1 | grep -v -i "userwarning\|super().__init"
echo "== full exit ${PIPESTATUS[0]} $(date -u '+%F %T')"
gtimeout 3h nice -n 10 $PY -u argcount.py --M=1 --A=0.5,6 --wf=0.2,3 --nA=22 --nwf=28 --procs=2 --out=$OUT --tag=M1_plant --plant=1.7,2.1 2>&1 | grep -v -i "userwarning\|super().__init"
echo "== plant exit ${PIPESTATUS[0]} $(date -u '+%F %T')"
