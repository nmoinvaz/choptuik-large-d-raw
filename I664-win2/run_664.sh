#!/usr/bin/env bash
# #664: the natural-test A/B on #603's four class B refusals (D 236.13 -> 237.13, 238.54 -> 239.51, 240.12 -> 240.89, 249.87 -> 250.47), as #644 does for 248.63 -> 249.39.
# For each: the stored base I603-win2/chain/anm_pin3_D<base>.npz, #603's flags (run_603.sh), --steps 1, --a0 = #603's a at that attempt (to full precision: the difference of the D of the refused attempt's
# target state and of its base, as saved in the states' meta; corrector_attempts.csv rounds a to 6 digits), once with --od_accept own and once with natural, 9 threads, BelowNormal, OPENBLAS_NUM_THREADS=1.
# Worktree D:/choptuik-i664 at origin/main 141d9d48 (newton_od prints |dz| to 3 digits and a line per refused trial, #666; printing only), venv-i600 (the #600 build, the kernel #603 runs on).
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I664-win2
cd /d/choptuik-i664/hp || exit 9
git merge-base --is-ancestor 141d9d48 HEAD || { echo "worktree D:/choptuik-i664 is older than 141d9d48" >&2; exit 9; }
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
# tag:base file:a0
for c in 236.13:D236.1312:1.0 238.54:D238.5375:0.9765625 240.12:D240.1244:0.762939453125 249.87:D249.8696:0.5960464477539062; do
  IFS=: read tag base a0 <<< "$c"
  [ -f $RAW/I603-win2/chain/anm_pin3_$base.npz ] || { echo "missing the $base state" >> $R/exits_664.txt; continue; }
  for acc in own natural; do
    echo "$tag $acc start a0 $a0 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_664.txt
    nice -n 5 "$PY" -u anm_run.py $RAW $R/${tag}_$acc --state I603-win2/chain/anm_pin3_$base.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 9 \
       --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
       --a0 $a0 --od_accept $acc > $R/${tag}_$acc.log 2>&1
    echo "$tag $acc exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_664.txt
  done
done
echo "664 all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_664.txt
