#!/usr/bin/env bash
# #461 probe: crawlK's command from crawlJ/anm_pin3_D242.4834.npz with --h_max $2, one attempt (--steps 1), output probe$1/, log probe$1.log, at main 2967dcd (the coordinator's order of 04:17 UTC:
# if the first |dz| stays near 1e-29 down to a 0.03125 the error comes from the re-seed or the base, not the step). usage: run_i461_probe.sh TAG HMAX   (125 0.125, 0625 0.0625, 03125 0.03125)
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I461-win2
S=I461-win2/crawlJ/anm_pin3_D242.4834.npz
cd /d/choptuik-i446/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "2967dcd" ] || { echo "worktree D:/choptuik-i446 is not at 2967dcd" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
echo "part probe$1 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from $S h_max $2" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/probe$1 --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max $2 --steps 1 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/probe$1.log 2>&1
echo "part probe$1 anm_run exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
