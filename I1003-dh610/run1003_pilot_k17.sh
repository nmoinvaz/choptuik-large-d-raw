#!/bin/bash
# #1003 pilot rerun on dh610 (the K 25 pilot hit its 1 h cap at order 19, no JSON): K 17 at J 1250, prec 1280, --fit phys --mf 6:12 --phys-prec 3840, --procs 8, nice 10, 1 h cap.
. "$(dirname "$0")/common1003.sh"
cd "$WT/solver/inner_amp" || exit 1
PY=$WTV/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
echo "# $(stamp) UTC pilot start, code $(git -C $WT rev-parse --short=8 HEAD), python-flint $($PY -c 'import flint; print(flint.__version__)'), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $OUT/exits_1003.txt
s=$(date +%s)
timeout -s TERM 3600 nice -n 10 $PY -u amp_flint_par.py 1.0 17 1250 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840 --out $OUT/pilot_K17_J1250.json > $OUT/pilot_K17_J1250.log 2>&1
rc=$?
echo "# $(stamp) UTC pilot exit $rc wall $(( $(date +%s) - s )) s" >> $OUT/exits_1003.txt
exit $rc
