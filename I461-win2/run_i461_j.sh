#!/usr/bin/env bash
# #461 crawlJ: crawlI restarted from its next saved state at main 2967dcd with --h_max 1.0 (keeping --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --qd_it 12 --tol_od 1e-60, the base polish
# ON, --held_o 1 --reseed_o 3 --od_junk 0), by the coordinator's order of 2026-11-11 01:55 UTC: the step then grows 0.5, 0.625, 0.78, 0.98, 1.0 while steps pass at the first try and
# holds wherever one is halved. Report the first refused attempt with its lines, and the step size the run settles at. Output crawlJ, log crawlJ.log, 18 threads, worktree
# D:/choptuik-i446 at 2967dcd. The 30 h cap counts from this start.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$(ls $R/crawlI/anm_pin3_D*.npz | sort -V | tail -n 1)
S=${S#$RAW/}
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "2967dcd" ] || { echo "worktree D:/choptuik-i446 is not at 2967dcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part J start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlJ --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 1.0 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/crawlJ.log 2>&1
rc=$?
echo "part J anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
