#!/bin/bash
# #1070 macm3b: the issue's hp/lowD_gamma.py command for one state, on venv-macm3-1058b, 6 threads, nice 10, capped by exact pid.
# Usage: run_1070.sh M128 | M160 [LAM0]       DRY=1 prints the command line and exits. CAP env: seconds (default 21600 = 6 h).
# TAG env (default empty) is appended to the output and log names (a rerun, e.g. TAG=_r2), so that records of runs do not mix.
MODE=$1; LAM0=$2
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1070-macm3
IN=$HOME/Source/choptuik-large-d-raw-749p/I927-mac/inputs
PY=$HOME/Source/venv-macm3-1058b/bin/python
CODE=$HOME/Source/choptuik-large-d-1070
CAP=${CAP:-21600}
case $MODE in M128|M160) ;; *) echo "usage: run_1070.sh M128|M160 [LAM0]"; exit 9;; esac
M=${MODE#M}
OUT=$O/lowD_gamma_D3.15_M$M$TAG.jsonl
STATE=$IN/lowDhm_x0.000625-0.9_D3.1500_M$M.npz
OPTS="--threads=6 --polish=2 --xtol=1e-11"
[ -n "$LAM0" ] && OPTS="$OPTS --lam0=$LAM0"
CMD="$PY -u hp/lowD_gamma.py $OUT $STATE $OPTS"
if [ -n "$DRY" ]; then echo "$CMD"; exit 0; fi
export PYTHONFAULTHANDLER=1
cd $CODE || exit 9
log() { echo "1070m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1070.txt; }
HK=$($PY -c "import hpkernel, multidouble, sys; print('hpkernel.__file__', hpkernel.__file__, 'isa', hpkernel.isa(), 'multidouble', multidouble.__file__, 'python', sys.version.split()[0])" 2>&1 | tr '\n' ' ')
log "$MODE$TAG start, code main $(git rev-parse HEAD), venv $PY: $HK; state blob $(git hash-object $STATE), cap $CAP s, command: $CMD"
t=$(date +%s)
caffeinate -is nice -n 10 $PY -u $O/capped_run.py $CAP $CMD > $O/run_$MODE$TAG.log 2>&1
rc=$?
log "$MODE$TAG exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
