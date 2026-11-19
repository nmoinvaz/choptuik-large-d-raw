#!/bin/bash
# #1003 main run on dh610: K 49 at J 1250 (the coordinator's order of 2026-11-19: --procs 12, 48 h cap, win2 runs J 1500), prec 1280, --fit phys --mf 6:12 --phys-prec 3840,
# nice 10. amp_flint_par.py writes its JSON only at the end (no checkpoint), so the log is the fallback: each odd order's sigma is printed there to 15 digits.
. "$(dirname "$0")/common1003.sh"
J=${1:-1250}; PROCS=${2:-12}
cd "$WT/solver/inner_amp" || exit 1
PY=$WTV/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
echo "# $(stamp) UTC K49 J$J start, code $(git -C $WT rev-parse --short=8 HEAD), python-flint $($PY -c 'import flint; print(flint.__version__)'), --procs $PROCS, load $(cut -d' ' -f1-3 /proc/loadavg)" >> $OUT/exits_1003.txt
s=$(date +%s)
timeout -s TERM 172800 nice -n 10 $PY -u amp_flint_par.py 1.0 49 $J 1280 --procs $PROCS --fit phys --mf 6:12 --phys-prec 3840 --out $OUT/sigF_w1.0000_K49_J${J}_p1280.json > $OUT/K49_J${J}.log 2>&1
rc=$?
echo "# $(stamp) UTC K49 J$J exit $rc wall $(( $(date +%s) - s )) s" >> $OUT/exits_1003.txt
exit $rc
