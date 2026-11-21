#!/bin/bash
# #1070 macm3b: the D 3.425 pair from T39's stored states (the coordinator's order, 2026-11-21): hp/lowD_gamma.py on each, the issue's flags.
# Usage: run_1070_D3425.sh M96|M128 LAM0      DRY=1 prints the command line and exits. CAP env: seconds (default 10800 = 3 h).
MODE=$1; LAM0=$2
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1070-macm3
IN=$HOME/Source/choptuik-large-d-raw-749p/T39-win/hp/data/lowD_states
PY=$HOME/Source/venv-macm3-1058b/bin/python
CODE=$HOME/Source/choptuik-large-d-1070
CAP=${CAP:-10800}
case $MODE in M96|M128) ;; *) echo "usage: run_1070_D3425.sh M96|M128 LAM0"; exit 9;; esac
[ -n "$LAM0" ] || { echo "LAM0 required"; exit 9; }
OUT=$O/lowD_gamma_D3.425_$MODE.jsonl
STATE=$IN/lowDvh41_D3.4250_$MODE.npz
CMD="$PY -u hp/lowD_gamma.py $OUT $STATE --threads=6 --polish=2 --xtol=1e-11 --lam0=$LAM0"
if [ -n "$DRY" ]; then echo "$CMD"; exit 0; fi
export PYTHONFAULTHANDLER=1
cd $CODE || exit 9
log() { echo "1070m D3.425 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1070.txt; }
HK=$($PY -c "import hpkernel, multidouble, sys; print('hpkernel.__file__', hpkernel.__file__, 'isa', hpkernel.isa(), 'multidouble', multidouble.__file__, 'python', sys.version.split()[0])" 2>&1 | tr '\n' ' ')
log "$MODE start, code main $(git rev-parse HEAD), venv $PY: $HK; state blob $(git hash-object $STATE), cap $CAP s, command: $CMD"
t=$(date +%s)
caffeinate -is nice -n 10 $PY -u $O/capped_run.py $CAP $CMD > $O/run_D3.425_$MODE.log 2>&1
rc=$?
log "$MODE exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
