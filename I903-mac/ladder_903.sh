#!/usr/bin/env bash
# #903 ladder at D 225.13 (the coordinator's comment of 2026-11-16 09:38 UTC): polish rungs in the horizon order from 130 to 250,
# each `--ks K --keep_plan 0 --steps 0 --save_base 1` from the previous rung's saved base, chain_nsr's flags F, 8 threads, nice 10.
# Step +10; a failed rung is retried at +5, then +2 (--ks is an integer, so +2 stands for +2.5); a failed +2 rung stops the ladder.
# After a success at a reduced step the next step doubles, up to +10. A rung succeeds when its base is saved and its octo-double
# polish ends converged with max|F| <= 1e-60. Each success gets rung_info.py (p_min, ln(p/p130), Delta - Delta_130). At 250,
# t250 runs two steps from its base. Worktree choptuik-large-d-xf-903 at main 663e3b2d, venv-314 with the #523 build (i599/site2).
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
RAW=$SP/raw-wt
O=$SP/i903/ladder
PY=/Users/nathan/venv-314/bin/python
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2:.
export PYTHONFAULTHANDLER=1
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 8 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
B130=$SP/i903/q130/base_pin3_D225.1312.npz
P130=9.7688e-19
cd /Users/nathan/Source/choptuik-large-d-xf-903/hp || exit 9
log() { echo "903L $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_ladder.txt; }
ok_rung() {  # log base
  [ -f "$2" ] || return 1
  l=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1)
  echo "$l" | grep -q ", converged" || return 1
  echo "$l" | grep -q "not converged" && return 1
  f=$(echo "$l" | sed -E 's/.*max\|F\| ([0-9.e+-]+),.*/\1/')
  $PY -c "import sys; sys.exit(0 if float('$f') <= 1e-60 else 1)"
}
log "main $(git rev-parse --short HEAD), from q130's base"
prev=130; base=$B130; step=10
while [ $prev -lt 250 ]; do
  K=$(( prev + step )); [ $K -gt 250 ] && K=250
  n=k${K}_from${prev}
  t=$(date +%s); log "$n start (step +$(( K - prev )))"
  nice -n 10 $PY -u anm_run.py $RAW $O/$n --state $base $F --ks $K --keep_plan 0 --steps 0 --D_max 226 --save_base 1 --allow_unraw > $O/$n.log 2>&1
  rc=$?; nb=$O/$n/base_pin3_D225.1312.npz
  if ok_rung $O/$n.log $nb; then
    log "$n converged (exit $rc, wall $(( $(date +%s) - t ))s)"
    nice -n 10 $PY -u $SP/i903/rung_info.py $nb $B130 $P130 $O/rungs.jsonl >> $O/rung_info.log 2>&1 || log "$n rung_info failed"
    prev=$K; base=$nb; step=$(( step * 2 )); [ $step -gt 10 ] && step=10
  else
    log "$n FAILED (exit $rc, wall $(( $(date +%s) - t ))s)"
    if [ $step -eq 10 ]; then step=5; elif [ $step -gt 2 ]; then step=2; else log "a failed +2 rung: the ladder stops at ks $prev"; exit 1; fi
  fi
done
log "ladder reached 250"
t=$(date +%s); log "t250 start"
nice -n 10 $PY -u anm_run.py $RAW $O/t250 --state $base $F --ks 250 --steps 2 --D_max 228 --allow_unraw > $O/t250.log 2>&1
log "t250 exit $? wall $(( $(date +%s) - t ))s"
