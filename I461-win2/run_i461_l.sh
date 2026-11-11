#!/usr/bin/env bash
# #461 crawlL: the chain from the accepted a 0.03125 probe state (probe03125/anm_pin3_D242.5146.npz, D 242.514649963) at main 2967dcd, crawlK's command with --a0 0.03125 --h_max 0.0625
# (the coordinator's order of 2026-11-11 17:01 UTC; a_grow 1.25, a_hold 1, lam_stall 0.04, qd_it 12, tol_od 1e-60, the base polish on). Output crawlL, log crawlL.log, 18 threads,
# worktree D:/choptuik-i446 at 2967dcd, 24 h cap. Stop rule (guard_l.sh): an attempt refused at a 0.0078125 or below. The data wanted: the accepted a and the first |dz| / a of every step against D.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/probe03125/anm_pin3_D242.5146.npz
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "2967dcd" ] || { echo "worktree D:/choptuik-i446 is not at 2967dcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part L start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S a0 0.03125 h_max 0.0625" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlL --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --a0 0.03125 --h_max 0.0625 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/crawlL.log 2>&1
rc=$?
echo "part L anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
