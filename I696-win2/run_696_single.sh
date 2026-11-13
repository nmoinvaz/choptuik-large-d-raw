#!/usr/bin/env bash
# #696, the coordinator's order 1794608760057-0: after the D 253.8043 ladder of run_696_k.sh has ended ("696 k D253 done" in exits_696.txt), at D 245.1366, 10 threads,
# the single-order ladder with --keep_plan 0: ks 132, 133, 134, ... each from the previous converged base (the first from r131k's base), stop at the first order that does not converge.
# Capped at ks 160 here (30 rungs, 10 to 20 min each), the coordinator extends it. Outputs D245/s<K>/, D245/s<K>.log, markers in exits_696.txt. STOP_S file stops rungs not yet started.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696b/hp || exit 9
git merge-base --is-ancestor 3d0ce152 HEAD || exit 9
until grep -q "696 k D253 done" $R/exits_696.txt; do sleep 20; done
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --keep_plan 0"
converged() { tail_line=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1); echo "$tail_line" | grep -q ", converged" && ! echo "$tail_line" | grep -q "not converged"; }
prev=r131k; prevdir=D245/r131k
for K in $(seq 132 160); do
  [ -f $R/STOP_S ] && { echo "696 D245 s$K not started, STOP_S file" >> $R/exits_696.txt; break; }
  b=$(ls $R/$prevdir/base_pin3_D*.npz 2>/dev/null | head -n 1)
  [ -n "$b" ] || { echo "696 D245 s$K no base from $prev, stops" >> $R/exits_696.txt; break; }
  mkdir -p $R/D245/s$K
  echo "696 D245 s$K start $(date -u '+%Y-%m-%d %H:%M:%S UTC') state I696-win2/$prevdir/$(basename $b) ks $K keep_plan 0" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/D245/s$K --state I696-win2/$prevdir/$(basename $b) $FLAGS --ks $K > $R/D245/s$K.log 2>&1
  rc=$?
  ok=$(converged $R/D245/s$K.log && echo yes || echo NO)
  echo "696 D245 s$K exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC') converged: $ok" >> $R/exits_696.txt
  if [ "$ok" = yes ]; then prev=s$K; prevdir=D245/s$K; else echo "696 D245 single-order ladder stops at ks $K (not converged), last converged $prev" >> $R/exits_696.txt; break; fi
done
echo "696 single-order ladder done, last converged $prev $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
