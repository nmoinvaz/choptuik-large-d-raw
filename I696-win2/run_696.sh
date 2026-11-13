#!/usr/bin/env bash
# #696: base polishes with the horizon series summed to ks 130 (control A), 300, 360 and r300's base again at 300 (control B), at D 245.1366 and D 253.8043, both D at once.
# usage: bash run_696.sh        (from anywhere; outputs go next to this script). Stop file I696-win2/STOP stops the runs that have not started.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696/hp || exit 9
git merge-base --is-ancestor 614211ab HEAD || exit 9
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 5 --corrector od --tol_od 1e-60 --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1"
first_F() { grep -m1 -E '^ +on 0: \|F\| ' "$1" | sed -E 's/^ +on 0: \|F\| ([0-9.e+-]+).*/\1/'; }
run() {  # dir tag state K
  local dd=$1 tag=$2 st=$3 k=$4
  [ -f $R/STOP ] && { echo "696 $dd $tag not started, STOP file" >> $R/exits_696.txt; return 9; }
  [ -f $RAW/$st ] || { echo "696 $dd $tag state $st missing" >> $R/exits_696.txt; return 9; }
  mkdir -p $R/$dd/$tag
  echo "696 $dd $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC') state $st ks $k" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/$dd/$tag --state $st $FLAGS --ks $k > $R/$dd/$tag.log 2>&1
  local rc=$?
  echo "696 $dd $tag exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC') first |F| $(first_F $R/$dd/$tag.log)" >> $R/exits_696.txt
  return $rc
}
chain() {  # dir state
  local dd=$1 st=$2 b
  run $dd r130 $st 130 || return
  run $dd r300 $st 300 || return
  # the check that --ks did something: r300's first |F| is at least 1e-30
  f=$(first_F $R/$dd/r300.log)
  if ! python3 -c "import sys; sys.exit(0 if float('$f') >= 1e-30 else 1)" 2>/dev/null; then
    echo "696 $dd r300 first |F| '$f' is below 1e-30: --ks did nothing, STOP" >> $R/exits_696.txt; touch $R/STOP; return 8
  fi
  run $dd r360 $st 360 || return
  b=$(ls $R/$dd/r300/base_pin3_D*.npz 2>/dev/null | head -n 1)
  [ -n "$b" ] || { echo "696 $dd r300 saved no base, p300 not run" >> $R/exits_696.txt; return 7; }
  run $dd p300 "I696-win2/$dd/r300/$(basename $b)" 300
}
echo "696 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
chain D245 I603-win2/chain/anm_pin3_D245.1366.npz &
chain D253 I603-win2/chain_nat/anm_pin3_D253.8043.npz &
wait
echo "696 all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
