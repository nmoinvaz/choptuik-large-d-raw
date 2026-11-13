#!/usr/bin/env bash
# #674: the strong-row chord (--od_strong 4, main 58628d94) on #603's class A refusals, A/B. Arm A: --od_accept natural --od_strong 4. Arm B (the control): --od_accept natural without --od_strong, at 244.637,
# 247.043 and 251.886 (248.630's natural arm is #644's run). From each base I603-win2/chain/anm_pin3_D<base>.npz at #603's own a for that attempt (attempt 0 of the step in its anm_run.jsonl, exact):
# 244.637 a 1.0, 247.043 a 0.9765625, 248.630 a 0.762939453125, 251.886 a 0.7275957614183426. #603's flags (run_603.sh) with --steps 1, 9 threads, BelowNormal (nice -n 5), OPENBLAS_NUM_THREADS=1.
# Worktree D:/choptuik-i674 at origin/main 58628d94, venv-i600 (the #600 build; a Python-only change). A refused first attempt halves a and the run goes on to the retry (as in #664).
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I674-win2
cd /d/choptuik-i674/hp || exit 9
git merge-base --is-ancestor 58628d94 HEAD || { echo "worktree D:/choptuik-i674 is older than 58628d94" >&2; exit 9; }
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
# tag:base file:a0:arms (A = natural + od_strong 4, B = natural)
for c in 244.637:D244.6366:1.0:AB 247.043:D247.0429:0.9765625:AB 248.630:D248.6298:0.762939453125:A 251.886:D251.8859:0.7275957614183426:AB; do
  IFS=: read tag base a0 arms <<< "$c"
  [ -f $RAW/I603-win2/chain/anm_pin3_$base.npz ] || { echo "missing the $base state" >> $R/exits_674.txt; continue; }
  for arm in A B; do
    case $arms in *$arm*) ;; *) continue ;; esac
    if [ $arm = A ]; then extra="--od_strong 4"; else extra=""; fi
    echo "$tag arm$arm start a0 $a0 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_674.txt
    nice -n 5 "$PY" -u anm_run.py $RAW $R/${tag}_arm$arm --state I603-win2/chain/anm_pin3_$base.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 9 \
       --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 \
       --a0 $a0 --od_accept natural $extra > $R/${tag}_arm$arm.log 2>&1
    echo "$tag arm$arm exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_674.txt
  done
done
echo "674 all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_674.txt
