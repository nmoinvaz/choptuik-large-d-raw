#!/bin/bash
# #928: the rates at eta 0.3, D 12.9375 and 13, which seg_qd.sh's list left out (states_in.py's first rule asked for
# the double-double stage's own convergence). The running job's leaf process is stopped meanwhile.
# (A first try from the interactive shell, zsh, passed the two state files as one argument and failed at once:
# out/failed/lam_eta0.3_D12.9375_13_qd_zsh_split.txt.)
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
PIDS=$(pgrep -f 'matter/sigma_ms/(mode_lam|run_eta)\.py')
[ -n "$PIDS" ] && kill -STOP $PIDS
trap '[ -n "$PIDS" ] && kill -CONT $PIDS' EXIT
echo "$(date -u '+%F %T') UTC the rates at eta 0.3, D 12.9375 and 13 start (stopped: $PIDS)" >> "$OUT/runs.log"
{ read -r P; read -r STATES; } < <($PY "$J/states_in.py" "$OUT" 0.3 12.875 13 "")
nice -n 10 $PY matter/sigma_ms/mode_lam.py $STATES --out "$OUT" --prev "$P" --threads 2 --gauge_window 1e-12 \
    --widths 1e-4,1e-3,1e-2,5e-2 > "$OUT/lam_eta0.3_D12.9375_13_qd.txt" 2>&1
echo "$(date -u '+%F %T') UTC lam eta0.3_D12.9375_13_qd exit $?" >> "$OUT/runs.log"
