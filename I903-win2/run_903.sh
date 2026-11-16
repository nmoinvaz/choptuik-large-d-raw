#!/usr/bin/env bash
# #903 pilot: the coordinator's three commands (comment on the issue, 2026-11-16), run one after another, with the corrections
# the coordinator confirmed by message on 2026-11-16 (04:3x UTC): --reseed 2 --reseed_q 1 on all three (chain_nsr's flags, lost from
# the issue comment's F), --save_base 1 on p130 and p160 (a --steps 0 run saves its polished base only with it), s160 from p160's base.
# Worktree D:/choptuik-i603r at 8479d915 (a515ab87 + --ks, #696), venv-i600, 9 threads. A run that exits non-zero, or whose base is not
# saved (the polish not adopted), stops the pilot.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I903-win2
S=T138-win2/chain/anm_pin3_D150.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /d/choptuik-i603r/hp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "903 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
run() { n=$1; shift; t=$(date +%s); log "$n start"; "$PY" -u anm_run.py $RAW $R/$n "$@" > $R/$n.log 2>&1; rc=$?; log "$n exit $rc wall $(( $(date +%s) - t ))s"; return $rc; }
[ -f $RAW/$S ] || { log "missing $S"; exit 9; }
log "main $(git rev-parse --short HEAD)"
run p130 --state $S $F --steps 0 --D_max 151 --save_base 1 || exit 1
[ -f $R/p130/base_pin3_D150.0000.npz ] || { log "p130 base not saved, stop"; exit 1; }
run p160 --state $S $F --steps 0 --D_max 151 --ks 160 --keep_plan 0 --save_base 1 || exit 1
[ -f $R/p160/base_pin3_D150.0000.npz ] || { log "p160 base not saved, stop"; exit 1; }
run s160 --state I903-win2/p160/base_pin3_D150.0000.npz $F --ks 160 --steps 2 --D_max 160 || exit 1
log "pilot done"
