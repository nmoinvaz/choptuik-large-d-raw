#!/usr/bin/env bash
# #696, the coordinator's order 1794605692736-0: after run_696_ladder.sh has finished (r131 and its --keep_plan 0 run), at D 245.1366, 10 threads, one after the other,
# the same command as r131 otherwise, in a worktree at main 16cfdfec (D:/choptuik-i696b; --elim_switch needs main 3d0ce152 or later):
#   r130x: --ks 130 --tol_od 1e-70   the control at the state's own ks, made to take a Newton step
#   r131s: --ks 131 --elim_switch 0  every point projected
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I696-win2
cd /d/choptuik-i696b/hp || exit 9
git merge-base --is-ancestor 3d0ce152 HEAD || exit 9
until grep -q "696 ladder script done" $R/exits_696.txt; do sleep 15; done
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --qd_it 20 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1"
S0=I603-win2/chain/anm_pin3_D245.1366.npz
# anm_run.py takes the FIRST occurrence of an option (args.index), so --tol_od is given once per run, not in FLAGS
run() {  # tag extra-args...
  local tag=$1; shift
  [ "$(echo "$FLAGS $*" | grep -o -e '--tol_od' | wc -l)" = 1 ] || { echo "696 D245 $tag: --tol_od not given exactly once, not run" >> $R/exits_696.txt; return 9; }
  mkdir -p $R/D245/$tag
  echo "696 D245 $tag start $(date -u '+%Y-%m-%d %H:%M:%S UTC') worktree main $(git rev-parse --short HEAD): $*" >> $R/exits_696.txt
  "$PY" -u anm_run.py $RAW $R/D245/$tag --state $S0 $FLAGS "$@" > $R/D245/$tag.log 2>&1
  echo "696 D245 $tag exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
}
run r130x --ks 130 --tol_od 1e-70
run r131s --ks 131 --tol_od 1e-60 --elim_switch 0
echo "696 x script done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_696.txt
