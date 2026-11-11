#!/usr/bin/env bash
# #522 part 2, one job: the attempt of a = 0.5 from crawlG D $1 (main 14dc386, 5 threads), then near_null_eq.py --plant=7 on the new state (0cce81e, 2 threads, below normal priority).
D=$1
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I522-win2
S=I461-win2/crawlG/anm_pin3_D$D.npz
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i446g/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "14dc386" ] || { echo "worktree D:/choptuik-i446g is not at 14dc386" >&2; exit 9; }
echo "attempt_D$D start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at 14dc386 from $S a 0.5" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/att_D$D --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max 0.5 --steps 1 --D_max 400 --threads 5 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --save_dz0 1 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/att_D$D.log 2>&1
echo "attempt_D$D anm_run exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
N=$(ls $R/att_D$D/anm_pin3_D*.npz 2>/dev/null | head -n 1)
[ -n "$N" ] || { echo "attempt_D$D no state saved (refused?)" >> $R/exits.txt; exit 0; }
Dn=$(basename $N .npz); Dn=${Dn#anm_pin3_}
cd /d/choptuik-i505/hp || exit 9
echo "eq_$Dn start $(date -u '+%Y-%m-%d %H:%M:%S UTC') from attempt_D$D" >> $R/exits.txt
nice -n 10 "$PY" -u near_null_eq.py $RAW I522-win2/att_D$D/anm_pin3_$Dn.npz --threads=2 --plant=7 --json=$R/eq_$Dn.json > $R/eq_$Dn.log 2>&1
echo "eq_$Dn exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
