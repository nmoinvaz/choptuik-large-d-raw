#!/bin/bash
# #903 (the coordinator, 2026-11-16 16:01 UTC and the hc after): a fixed-order chain at horizon order 135 on macm3b.
# Rung: anm_run.py with chain_nsr's flags F (6 threads) --ks 135 --keep_plan 0 --steps 0 --D_max 226 --save_base 1 from q130's base.
# If its octo-double polish converges to max|F| <= 1e-60 with the base saved (the ok_rung test of I903-mac/ladder_903.sh), the chain
# from that base: --ks 135 --keep_plan 1 --steps 400 --D_max 262, into I903-macm3/chain_k135. Else stop.
# Code: worktree choptuik-large-d-903m at main 5897ee28 (python), venv-macm3-main with the 1f3cda09 hpkernel (no Solver.series_o,
# so anm_run forms the series by the jets, with a notice), nice 10 under caffeinate.
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I903-macm3
PY=$HOME/Source/venv-macm3-main/bin/python
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 6 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd $HOME/Source/choptuik-large-d-903m/hp || exit 9
log() { echo "903m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_k135.txt; }
ok_rung() {
  [ -f "$2" ] || return 1
  l=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1)
  echo "$l" | grep -q ", converged" || return 1
  echo "$l" | grep -q "not converged" && return 1
  f=$(echo "$l" | sed -E 's/.*max\|F\| ([0-9.e+-]+),.*/\1/')
  $PY -c "import sys; sys.exit(0 if float('$f') <= 1e-60 else 1)"
}
log "main $(git rev-parse --short=8 HEAD), hpkernel from the 1f3cda09 build, from q130's base"
t=$(date +%s); log "rung135 start"
caffeinate -is nice -n 10 $PY -u anm_run.py $RAW $O/rung135 --state I903-mac/q130/base_pin3_D225.1312.npz $F --ks 135 --keep_plan 0 --steps 0 --D_max 226 --save_base 1 > $O/rung135.log 2>&1
rc=$?
log "rung135 exit $rc wall $(( $(date +%s) - t ))s"
if ok_rung $O/rung135.log $O/rung135/base_pin3_D225.1312.npz; then
  log "rung135 converged"
else
  log "rung135 FAILED, no chain"
  exit 1
fi
t=$(date +%s); log "chain_k135 start"
caffeinate -is nice -n 10 $PY -u anm_run.py $RAW $O/chain_k135 --state I903-macm3/rung135/base_pin3_D225.1312.npz $F --ks 135 --keep_plan 1 --steps 400 --D_max 262 > $O/chain_k135.log 2>&1
log "chain_k135 exit $? wall $(( $(date +%s) - t ))s"
