#!/usr/bin/env bash
# #783: the order-132 climb between w = 1/4 and 1/2 at D 245.1366, from #744's w25 base, with run_744.sh's flags at 6
# threads (beside #603's chain and #709) and --log_proj 1 (logging only: #743 reproduced s132's lines with it). Worktree
# D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744. The order, fixed before the run:
#   w375  (w = 3/8) from w25's base;
#   if it converges: w4375 (7/16) from w375's base, then, if that converges, w5b (1/2) from w4375's base;
#   if it does not: w3125 (5/16) from w25's base.
# A rung converges by its own last "octo-double Newton" line.
PY=/c/Users/nathan/Source/venv-i744/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I783-win2
cd /d/choptuik-i744/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "c6468d2b" ] || { echo "worktree is not at c6468d2b" >&2; exit 9; }
"$PY" -c "import sys; from hpkernel._hpkernel import Solver; sys.exit(0 if hasattr(Solver, 'set_ks_w') else 1)" || { echo "venv-i744's hpkernel has no set_ks_w" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 6 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --log_proj 1"
log() { echo "783 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_783.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
base_of() { ls $1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
run() {  # tag state w
  mkdir -p $R/$1
  log "$1 start, state $2, ks_w $3"
  "$PY" -u anm_run.py $RAW $R/$1 --state $2 $FLAGS --qd_it 20 --ks 132 --ks_w $3 > $R/$1.log 2>&1
  log "$1 exit $? converged: $(converged $R/$1.log && echo yes || echo NO)"
}
rel() { b=$(base_of $RAW/$1); echo "${b#$RAW/}"; }
B25=$(rel I744-win2/w25); [ -n "$B25" ] || { log "no w25 base in I744-win2"; exit 9; }
run w375 $B25 0.375
if converged $R/w375.log; then
  run w4375 $(rel I783-win2/w375) 0.4375
  converged $R/w4375.log && run w5b $(rel I783-win2/w4375) 0.5
else
  run w3125 $B25 0.3125
fi
"$PY" -I $R/table_783.py $R > $R/table_783.txt 2>&1; log "table exit $?"
log "all done"
