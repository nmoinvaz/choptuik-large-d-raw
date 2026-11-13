#!/usr/bin/env bash
# #696, the coordinator's order 1794609060270-0, 10 threads, worktree D:/choptuik-i696b at main 16cfdfec (--elim_switch needs 3d0ce152 or later), all with --keep_plan 0 --elim_switch 0:
#  1. wait until the single-order ladder (run_696_single.sh) has stopped after rung 132 (STOP_S) -> "696 single-order ladder done" in exits_696.txt
#  2. r130k-s at D 253.8043: --ks 130
#  3. if it converged, D 253.8043's coarse ladder from its base: 131 135 145 160 200 250 300, each from the previous converged base, stop at the first failure (tags r<K>s)
#  4. then the single-order ladder at D 245.1366 resumes, --elim_switch 0 from rung 133 on, from rung 132's base (tags s133, s134, ...; if rung 132 did not converge, it is run again as s132e with the switch from r131k's base), stop at the first failure, cap ks 160
# anm_run.py takes the FIRST occurrence of an option, so --tol_od, --keep_plan and --elim_switch are each given once, in FLAGS.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696b/hp || exit 9
git merge-base --is-ancestor 3d0ce152 HEAD || exit 9
until grep -q "696 single-order ladder done" $R/exits_696.txt; do sleep 15; done
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --keep_plan 0 --elim_switch 0"
for o in tol_od keep_plan elim_switch; do [ "$(echo "$FLAGS" | grep -o -e "--$o" | wc -l)" = 1 ] || { echo "696 s-script: --$o not exactly once in FLAGS" >> $R/exits_696.txt; exit 9; }; done
converged() { tail_line=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1); echo "$tail_line" | grep -q ", converged" && ! echo "$tail_line" | grep -q "not converged"; }
run() {  # dir tag state K
  local dd=$1 tag=$2 st=$3 k=$4
  [ -f $R/STOP_T ] && { echo "696 $dd $tag not started, STOP_T file" >> $R/exits_696.txt; return 9; }
  mkdir -p $R/$dd/$tag
  echo "696 $dd $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC') state $st ks $k keep_plan 0 elim_switch 0" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/$dd/$tag --state $st $FLAGS --ks $k > $R/$dd/$tag.log 2>&1
  local rc=$?
  echo "696 $dd $tag exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC') converged: $(converged $R/$dd/$tag.log && echo yes || echo NO)" >> $R/exits_696.txt
  return $rc
}
base_of() { ls $R/$1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
# 2 and 3
run D253 r130ks I603-win2/chain_nat/anm_pin3_D253.8043.npz 130
if converged $R/D253/r130ks.log; then
  prev=r130ks
  for K in 131 135 145 160 200 250 300; do
    b=$(base_of D253/$prev); [ -n "$b" ] || { echo "696 D253 r${K}s no base from $prev, stops" >> $R/exits_696.txt; break; }
    run D253 r${K}s "I696-win2/D253/$prev/$(basename $b)" $K
    if converged $R/D253/r${K}s.log; then prev=r${K}s; else echo "696 D253 coarse ladder stops at ks $K (not converged), last converged $prev" >> $R/exits_696.txt; break; fi
  done
  echo "696 D253 coarse ladder with elim_switch 0 done, last converged $prev" >> $R/exits_696.txt
else
  echo "696 D253 r130ks did not converge, coarse ladder not run" >> $R/exits_696.txt
fi
echo "696 s-script D253 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
# 4
if converged $R/D245/s132.log; then prevdir=D245/s132; prevtag=s132
else
  run D245 s132e I696-win2/D245/r131k/base_pin3_D245.1366.npz 132
  if converged $R/D245/s132e.log; then prevdir=D245/s132e; prevtag=s132e; else echo "696 D245 s132e did not converge, single-order ladder not resumed" >> $R/exits_696.txt; echo "696 s-script done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt; exit 0; fi
fi
for K in $(seq 133 160); do
  b=$(base_of $prevdir); [ -n "$b" ] || { echo "696 D245 s$K no base from $prevtag, stops" >> $R/exits_696.txt; break; }
  run D245 s$K "I696-win2/$prevdir/$(basename $b)" $K
  if converged $R/D245/s$K.log; then prevtag=s$K; prevdir=D245/s$K; else echo "696 D245 single-order ladder (elim_switch 0) stops at ks $K (not converged), last converged $prevtag" >> $R/exits_696.txt; break; fi
done
echo "696 s-script done, last converged $prevtag $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
