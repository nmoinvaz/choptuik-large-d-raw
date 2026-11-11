#!/usr/bin/env bash
# #516 part 2: one attempt from crawlJ D 239.5375 at a = 0.268799963 to D 239.8063 (the first chain's crawlE D), crawlK's command, 18 threads, main 14dc386 (Python only).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I516-win2
S=I461-win2/crawlJ/anm_pin3_D239.5375.npz
cd /d/choptuik-i446g/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "14dc386" ] || { echo "worktree D:/choptuik-i446g is not at 14dc386" >&2; exit 9; }
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
echo "attempt start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at 14dc386 from $S a 0.268799963" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/attempt --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.268799963 --steps 1 --D_max 400 --threads 18 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --save_dz0 1 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/attempt.log 2>&1
echo "attempt anm_run exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
