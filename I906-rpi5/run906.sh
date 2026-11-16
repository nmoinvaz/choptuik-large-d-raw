#!/bin/bash
# #906 on rpi5: dinf_check.py's two checks of Delta_inf (Bulirsch-Stoer and Akaike-averaged fits), each on the six
# plants of planted_dinf.py and then the real points, with one mutation each that must fail.
# Usage: bash run906.sh PY WT ROOT  (the venv's python, a worktree at main 49bfccec or later, the raw clone)
PY=$1; WT=$2; ROOT=$3
R=$ROOT/I906-rpi5
cd $WT/hp || exit 9
git merge-base --is-ancestor 49bfccec HEAD || { echo "STOP: the worktree is older than 49bfccec"; exit 9; }
mkdir -p $R
log() { echo "906 $* $(date -u '+%F %T') UTC" >> $R/exits_906.txt; }
{ echo "commit $(git rev-parse --short=8 HEAD)"; $PY -c "import mpmath, sys, platform; print('mpmath', mpmath.__version__, platform.platform(), 'python', sys.version.split()[0])"; } > $R/env.txt 2>&1
run() {  # name, required exit status, then the arguments
  local name=$1 want=$2; shift 2
  log "$name start"
  local t=$(date +%s)
  nice -n 10 $PY -u dinf_check.py "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc (required $want) wall $(( $(date +%s) - t )) s"
}
run bst 0 bst
run bst_omega2 1 bst --mutate omega2
run aic 0 aic
run aic_noweight 1 aic --mutate noweight
log done
