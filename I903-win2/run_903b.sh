#!/usr/bin/env bash
# #903, the second pilot (coordinator's message, 2026-11-16 05:0x UTC): the polish at D 150 at --ks 250 and at --ks 410, one after
# another, p410 even if p250 fails. Same S, F, worktree (D:/choptuik-i603r at 8479d915), venv-i600 and 9 threads as run_903.sh, which it
# follows; it only chains the two commands. A missing base is logged, it does not stop the second run.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I903-win2
S=T138-win2/chain/anm_pin3_D150.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /d/choptuik-i603r/hp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "903b $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u anm_run.py $RAW $R/$n "$@" > $R/$n.log 2>&1; rc=$?; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
[ -f $RAW/$S ] || { log "missing $S"; exit 9; }
log "main $(git rev-parse --short HEAD)"
run p250 --state $S $F --steps 0 --D_max 151 --ks 250 --keep_plan 0 --save_base 1
[ -f $R/p250/base_pin3_D150.0000.npz ] || log "p250 base not saved"
run p410 --state $S $F --steps 0 --D_max 151 --ks 410 --keep_plan 0 --save_base 1
[ -f $R/p410/base_pin3_D150.0000.npz ] || log "p410 base not saved"
log "second pilot done"
