#!/bin/bash
# #597: hp/modecount_check.py on the new and the old build, 2 threads, nice 10, from hp/ of the worktree.
# No cut: up6_D30.0688.npz (M 32); kfreeze: up7_D40.0201.npz (M 32, kf 13, setup's default from D 35 on).
# Regression: #473's cache (I473-macm3/data/modecount_D30.0688_M64_evals.jsonl, 544 determinants) on #473's M 64 state
# (sha256 92f49438..., the one #609 used), --quick, 8 points; the control of checks 2 and 5: --mutate=dmat.
source "$(dirname "$0")/env597.sh"
cd "$WT/hp" || exit 1
mkdir -p "$RAW/check"
CACHE=$RAW/check/modecount_D30.0688_M64_evals_I473.jsonl
S64=$STATES/modecount_state_D30.0688_M64.npz
run() {  # build name args...
  local b=$1 n=$2
  shift 2
  $b modecount_check.py "$@" --threads=2 --out="$RAW/check/${b}_$n.jsonl" > "$RAW/check/${b}_$n.log" 2>&1
  echo "check ${b}_$n exit $? at $(date -u +%FT%TZ)" >> "$RAW/exits.txt"
}
case "$1" in
  nocut)
    for b in new old; do run $b D30_M32 data/states/up6_D30.0688.npz; done
    run new D30_M32_mutate_dmat data/states/up6_D30.0688.npz --quick --mutate=dmat ;;
  kf)
    for b in new old; do run $b D40_M32_kf13 data/states/up7_D40.0201.npz; done ;;
  regress)
    for b in new old; do run $b D30_M64_regress473 "$S64" --quick --regress="$CACHE" --regress_n=8; done
    run new D30_M64_regress473_mutate_dmat "$S64" --quick --regress="$CACHE" --regress_n=2 --mutate=dmat ;;
esac
