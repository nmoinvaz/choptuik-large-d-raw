#!/bin/bash
# Usage: run_case.sh NAME LO HI JSONL NPY [EXTRA ARGS...]
# Runs d18_secant.py run for one state under a 14400 s cap, 2 BLAS-free Rust threads, nice 10, caffeinate.
set -u
NAME=$1; LO=$2; HI=$3; JSONL=$4; NPY=$5; shift 5
HERE=$(cd "$(dirname "$0")" && pwd)
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=2
source "$HOME/Source/venv-macm3-1058b/bin/activate"
cd "$HOME/Source/choptuik-ell1fast/solver/matter"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') start $NAME bracket $LO $HI pid $$"
caffeinate -is nice -n 10 python3 "$HERE/common/capped_run.py" 14400 python d18_secant.py run "$JSONL" "$NPY" 23.0 "$LO" "$HI" "$HERE/$NAME.jsonl" --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2 "$@"
RC=$?
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') end $NAME exit=$RC"
echo "$RC" > "$HERE/$NAME.exit"
