#!/usr/bin/env bash
# #461 crawlI: restart from the D 232.63125 state (crawlG's, crawlH saved none) at main 2967dcd ("the chain keeps a step found by halving, and ends a stalled attempt":
# hp/anm_run.py and hp/octo_corrector.py only), by the coordinator's order of 2026-11-11 00:51 UTC (it replaces the options of 00:27 UTC): crawlH's command with --tol_od 1e-60
# --h_max 0.5 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --qd_it 12 and the base polish ON (no --base_polish 0); --held_o 1 --reseed_o 3 --od_junk 0 kept. Output crawlI, log
# crawlI.log, 18 threads, worktree D:/choptuik-i446 detached at 2967dcd. The 30 h cap counts from this start.
# Reading rule (written before the run): 1. the log prints "the base keeps its stored plan", then the polish: its Newton lines (report the first |dz|, the base's offset along the weak
# direction, predicted about 1e-23) and "octo-double Newton: k steps, max|F| ..., converged" below 1e-60; if the polish does not converge or "base polish not adopted" prints, the reading is
# wrong: report and let the run go on. 2. The first step from the polished base: a first |dz| near 1e-30 at a 0.5 and at most 4 Newton steps, accepted; a first |dz| near 4e-26 again
# means the reading is wrong. 3. Report both at once; the hourly table with each step's final max|F| (every one below 1e-60). The step rule and the stall line are checked as before.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/crawlG/anm_pin3_D232.6312.npz
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "2967dcd" ] || { echo "worktree D:/choptuik-i446 is not at 2967dcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
t=$(date +%s)
echo "part I start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/crawlI --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.5 --steps 400 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/crawlI.log 2>&1
rc=$?
echo "part I anm_run --steps 400 exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
