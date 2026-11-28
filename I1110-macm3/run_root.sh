#!/bin/bash
# Usage: run_root.sh LO HI OUTNAME   (#1110 step 7: root of the chord035 state; 2 Rust threads, nice 10, caffeinate, 14400 s cap)
set -u
LO=$1; HI=$2; NAME=$3
HERE=$(cd "$(dirname "$0")" && pwd)
export RAYON_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 D18_DIR=$HOME/Source/choptuik-ell1fast/solver/matter
source "$HOME/Source/venv-macm3-1058b/bin/activate"
cd "$HOME/Source/choptuik-ell1fast/solver/matter"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') start $NAME bracket $LO $HI pid $$"
caffeinate -is nice -n 10 python3 "$HERE/common/capped_run.py" 14400 python i1101_weakdir.py root "$HERE/sol_chord035_D23.0000.npy" "$LO" "$HI" "$HERE/$NAME.jsonl" --tol=1e-6 --b12=rust --b12_threads=2
RC=$?
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') end $NAME exit=$RC"
echo "$RC" > "$HERE/$NAME.exit"
