#!/usr/bin/env bash
# #903 restart (coordinator's hc, 2026-11-18 ~07:33 UTC): the ks 260 rung from D 237.527 failed, so ks_chain.py (main 3b60968f, worktree D:/choptuik-i603r) restarts from
# #948's converged ks 280 base at D 232 (copied to I903-win2/start948/) with --mult 4.4 --pad -249, run_ks_chain.sh's flags, 9 threads, OUT I903-win2/ks_chain2.
# It only runs the coordinator's command and logs its exit. The flag is "--pad -249" in two words because this ks_chain.py rejects "--pad=-249".
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I903-win2
S=I903-win2/start948/base_pin3_D232.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd /d/choptuik-i603r/hp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "903e $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_903.txt; }
[ -f $RAW/$S ] || { log "missing $S"; exit 9; }
log "ks_chain start from $S, --mult 4.4 --pad -249, D_stop 400, OUT I903-win2/ks_chain2, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u ks_chain.py $RAW $R/ks_chain2 --state $S --D_stop 400 --mult 4.4 --pad -249 -- $F --steps 400 >> $R/ks_chain2.log 2>&1
rc=$?
log "ks_chain2 exit $rc wall $(( $(date +%s) - t ))s"
