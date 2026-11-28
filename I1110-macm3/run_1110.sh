#!/bin/bash
# #1110 steps 1 to 6 (jac, svd, chord 0.35, chord 0.34 control, coords x2), 6 threads, nice 10, caffeinate, each capped at 7200 s; stops at the first failing step.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
RAW=$(cd "$HERE/.." && pwd)
LOCAL=$HOME/Source/I1110-macm3-local
IN=$RAW/I1101-dh170/in
REC=$IN/l1kc127k070w2.jsonl
ST=$IN/sol_l1kc127k070w2_D23.0000.npy
R2=$IN/sol_l1kc127k035w2_D23.0000.npy
export OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 D18_DIR=$HOME/Source/choptuik-ell1fast/solver/matter
source "$HOME/Source/venv-macm3-1058b/bin/activate"
cd "$HOME/Source/choptuik-ell1fast/solver/matter"
step() {
  local name=$1; shift
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') start $name" | tee -a "$HERE/exits_1110.txt"
  caffeinate -is nice -n 10 python3 "$HERE/common/capped_run.py" 7200 python i1101_weakdir.py "$@" > "$HERE/$name.log" 2>&1
  local rc=$?
  echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') end $name exit=$rc" | tee -a "$HERE/exits_1110.txt"
  [ $rc -eq 0 ] || { echo "stopped at $name" | tee -a "$HERE/exits_1110.txt"; exit $rc; }
}
step jac_r0 jac "$REC" "$ST" 23.0 "$LOCAL/jac_r0.npz" --pin=90d3e655,d1a3a641
step svd_r0 svd "$LOCAL/jac_r0.npz" "$LOCAL/svd_r0.npz"
step chord035 chord "$LOCAL/svd_r0.npz" "$REC" "$ST" 23.0 kappa=0.35 "$HERE/sol_chord035_D23.0000.npy"
step chord034 chord "$LOCAL/svd_r0.npz" "$REC" "$ST" 23.0 kappa=0.34 "$HERE/sol_chord034_D23.0000.npy"
step coords_r0 coords "$LOCAL/svd_r0.npz" "$ST" chord035="$HERE/sol_chord035_D23.0000.npy"
step coords_r2 coords "$LOCAL/svd_r0.npz" "$R2" chord035="$HERE/sol_chord035_D23.0000.npy"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') chain done" | tee -a "$HERE/exits_1110.txt"
