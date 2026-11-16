#!/usr/bin/env bash
# #903 Mac pilot (the coordinator's comment of 2026-11-16 08:08 UTC): the jump from horizon order 130 to 250 at D 225.13 from
# I603-win2/base/base_pin3_D225.1312.npz, three anm_run.py runs one after another with chain_nsr's flags F (--reseed 2
# --reseed_q 1 included) at --threads 8, nice 10. Worktree choptuik-large-d-xf-903 at main 663e3b2d, venv-314 with the #523 build
# (i599/site2). Output to the scratchpad (--allow_unraw), copied into the raw folder I903-mac for commits. A run that exits
# non-zero, or whose base is not saved, stops the pilot.
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
RAW=$SP/raw-wt
O=$SP/i903
PY=/Users/nathan/venv-314/bin/python
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export PYTHONFAULTHANDLER=1
S=I603-win2/base/base_pin3_D225.1312.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 8 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /Users/nathan/Source/choptuik-large-d-xf-903/hp || exit 9
log() { echo "903 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_903.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; nice -n 10 "$PY" -u anm_run.py $RAW $O/$n "$@" --allow_unraw > $O/$n.log 2>&1; rc=$?; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
[ -f $RAW/$S ] || { log "missing $S"; exit 9; }
log "main $(git rev-parse --short HEAD)"
run q130 --state $S $F --steps 0 --D_max 226 --save_base 1 || exit 1
[ -f $O/q130/base_pin3_D225.1312.npz ] || { log "q130 base not saved, stop"; exit 1; }
run q250 --state $S $F --steps 0 --D_max 226 --save_base 1 --ks 250 --keep_plan 0 || exit 1
[ -f $O/q250/base_pin3_D225.1312.npz ] || { log "q250 base not saved, stop"; exit 1; }
run t250 --state $O/q250/base_pin3_D225.1312.npz $F --ks 250 --steps 2 --D_max 228 || exit 1
log "pilot done"
