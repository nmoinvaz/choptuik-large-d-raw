#!/usr/bin/env bash
# #696, the coordinator's order 1794604510978-0: r131 first at D 245.1366 only (10 threads), from the chain's state, then
#   r131 converged     -> climb the ks ladder 135 145 160 200 250 300, each from the previous converged base, stop at the first rung that does not converge;
#   r131 did not       -> one more r131 with --keep_plan 0 (does the stored plan carry the old ks), and stop.
# Converged = the log's "octo-double Newton: N steps, max|F| X, converged". Outputs D245/r<K>/, D245/r<K>.log, exits_696.txt.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696/hp || exit 9
git merge-base --is-ancestor 614211ab HEAD || exit 9
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1"
S0=I603-win2/chain/anm_pin3_D245.1366.npz
converged() { grep -E "octo-double Newton: [0-9]+ steps, max\|F\| [0-9.e+-]+, converged" "$1" | tail -n 1 | grep -q converged && ! grep -E "octo-double Newton" "$1" | tail -n 1 | grep -q "not converged"; }
run() {  # tag state K extra
  local tag=$1 st=$2 k=$3 extra=$4
  mkdir -p $R/D245/$tag
  echo "696 D245 $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC') state $st ks $k $extra" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/D245/$tag --state $st $FLAGS --ks $k $extra > $R/D245/$tag.log 2>&1
  local rc=$?
  echo "696 D245 $tag exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
  return $rc
}
base_of() { ls $R/D245/$1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
run r131 $S0 131 ""
if converged $R/D245/r131.log; then
  prev=r131
  for K in 135 145 160 200 250 300; do
    b=$(base_of $prev); [ -n "$b" ] || { echo "696 D245 r$K no base from $prev, ladder stops" >> $R/exits_696.txt; break; }
    run r$K "I696-win2/D245/$prev/$(basename $b)" $K ""
    if converged $R/D245/r$K.log; then prev=r$K; else echo "696 D245 ladder stops at ks $K (not converged), last converged $prev" >> $R/exits_696.txt; break; fi
  done
  echo "696 D245 ladder done, last converged $prev" >> $R/exits_696.txt
else
  echo "696 D245 r131 did not converge: one more with --keep_plan 0, then stop" >> $R/exits_696.txt
  run r131k $S0 131 "--keep_plan 0"
fi
echo "696 ladder script done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
