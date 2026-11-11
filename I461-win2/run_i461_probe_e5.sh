#!/usr/bin/env bash
# #461 A/B probe at main e5bbdcd (the re-seed rung fix, hp/reseed.py): crawlK's command, one attempt (--steps 1) with --h_max $2 from the state $3, output probeE$1/, log probeE$1.log.
# Python only: the interpreter and its hpkernel build are venv-t126's as in the other probes; the worktree D:/choptuik-i446e is at e5bbdcd (the coordinator's order of 17:50 UTC).
# usage: run_i461_probe_e5.sh TAG HMAX STATE   (E0625 0.0625 I461-win2/crawlJ/anm_pin3_D242.4834.npz ; E015625 0.015625 I461-win2/probe03125/anm_pin3_D242.5146.npz)
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=$3
cd /d/choptuik-i446e/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "e5bbdcd" ] || { echo "worktree D:/choptuik-i446e is not at e5bbdcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
echo "part probe$1 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at e5bbdcd from $S h_max $2" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/probe$1 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max $2 --steps 1 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/probe$1.log 2>&1
echo "part probe$1 anm_run exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
