#!/usr/bin/env bash
# #461 crawlK: crawlJ restarted from its next saved state at main 2967dcd with --h_max 0.5 (crawlJ's command, the rest unchanged), by the coordinator's order of 2026-11-11 03:43 UTC
# (the refused a 0.95 attempts cost 9 Newton steps and the count rises with D at a fixed step). Output crawlK, log crawlK.log, 18 threads, worktree D:/choptuik-i446 at 2967dcd, 30 h cap.
# Stop rules, any one stops the run (guard_k.sh does it): a_max under 2.0, |z_N| above 1e-24, a step that needs more than 12 Newton steps or is refused at a 0.25 or below.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlJ/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "2967dcd" ] || { echo "worktree D:/choptuik-i446 is not at 2967dcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part K start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlK --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.5 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/crawlK.log 2>&1
rc=$?
echo "part K anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
