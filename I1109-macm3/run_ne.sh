#!/bin/bash
# Stage 1e step 1: nonlinear elimination from R0 (OUTDIR = ne/ beside this script), 6 threads, nice 10, caffeinate, 21600 s cap.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$HERE/.." && pwd)
export OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6
source "$HOME/Source/venv-macm3-1058b/bin/activate"
cd "$HOME/Source/choptuik-ell1fast/solver/matter"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') start ne pid $$"
caffeinate -is nice -n 10 python3 "$HERE/common/capped_run.py" 21600 python i1101_weakdir.py ne "$RAW/I1101-dh170/in/l1kc127k070w2.jsonl" "$RAW/I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy" 23.0 "$HERE/ne/" --outer=6
RC=$?
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') end ne exit=$RC"
echo "$RC" > "$HERE/ne.exit"
