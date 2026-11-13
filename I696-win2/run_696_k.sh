#!/usr/bin/env bash
# #696, the coordinator's order 1794606998584-0: with --keep_plan 0 (the stored plan was the fault of r131), 10 threads, from the chain's state:
#   per D, r130k (--ks 130, the control: Delta(130, new plan) - Delta(130, stored plan)), then the ladder 135 145 160 200 250 300, each rung from the previous converged base,
#   stop at the first rung that does not converge. D 245.1366 first, then D 253.8043. Worktree D:/choptuik-i696b at main 16cfdfec (elim_switch default 1e-15 as before).
# anm_run.py takes the FIRST occurrence of an option, so --tol_od and --keep_plan are given once.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696b/hp || exit 9
git merge-base --is-ancestor 3d0ce152 HEAD || exit 9
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --keep_plan 0"
converged() { tail_line=$(grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1); echo "$tail_line" | grep -q ", converged" && ! echo "$tail_line" | grep -q "not converged"; }
run() {  # dir tag state K
  local dd=$1 tag=$2 st=$3 k=$4
  [ -f $R/STOP_K ] && { echo "696 $dd $tag not started, STOP_K file" >> $R/exits_696.txt; return 9; }
  [ -f $RAW/$st ] || { echo "696 $dd $tag state $st missing" >> $R/exits_696.txt; return 9; }
  mkdir -p $R/$dd/$tag
  echo "696 $dd $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC') state $st ks $k keep_plan 0 worktree main $(git rev-parse --short HEAD)" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/$dd/$tag --state $st $FLAGS --ks $k > $R/$dd/$tag.log 2>&1
  local rc=$?
  echo "696 $dd $tag exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC') converged: $(converged $R/$dd/$tag.log && echo yes || echo NO)" >> $R/exits_696.txt
  return $rc
}
base_of() { ls $R/$1/$2/base_pin3_D*.npz 2>/dev/null | head -n 1; }
ladder() {  # dir state
  local dd=$1 st=$2 prev=r130k K b
  run $dd r130k $st 130
  converged $R/$dd/r130k.log || { echo "696 $dd r130k did not converge, ladder not run" >> $R/exits_696.txt; return; }
  for K in 135 145 160 200 250 300; do
    b=$(base_of $dd $prev); [ -n "$b" ] || { echo "696 $dd r${K}k no base from $prev, ladder stops" >> $R/exits_696.txt; break; }
    run $dd r${K}k "I696-win2/$dd/$prev/$(basename $b)" $K
    if converged $R/$dd/r${K}k.log; then prev=r${K}k; else echo "696 $dd ladder stops at ks $K (not converged), last converged $prev" >> $R/exits_696.txt; break; fi
  done
  echo "696 $dd ladder done, last converged $prev" >> $R/exits_696.txt
}
ladder D245 I603-win2/chain/anm_pin3_D245.1366.npz
echo "696 k D245 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
ladder D253 I603-win2/chain_nat/anm_pin3_D253.8043.npz
echo "696 k D253 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
