#!/bin/bash
# One chain step (#603's anm_run.py command with --steps 1) on the #604 build (main e835d94) and then the #614 build (main 3c35f0c),
# the same 12 threads, one after the other, nothing else running, nice 10. State: I603-win2/base/base_pin3_D225.1312.npz (copied to base/).
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I614-dh370
S=I614-dh370/base/base_pin3_D225.1312.npz
step() {  # name worktree
  local name=$1 wt=$2
  cd "$wt/hp" && . ../.venv/bin/activate
  export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1
  mkdir -p $OUT/chain_$name
  local t=$(date +%s)
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $(git rev-parse HEAD), hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), sha256 $(sha256sum $(python -c 'import hpkernel;print(hpkernel.__file__.replace("__init__.py","_hpkernel*.so"))' ) 2>/dev/null | cut -c1-16 | head -1)" > $OUT/timing_$name.log
  nice -n 10 python -u anm_run.py $RAW $OUT/chain_$name --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
     --h_max 1.0 --steps 1 --D_max 400 --threads 12 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 \
     --held_o 1 --reseed_o 3 --save_pred 1 >> $OUT/timing_$name.log 2>&1
  local rc=$?
  echo "exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%H:%M:%S') UTC" >> $OUT/timing_$name.log
}
step b604 /home/nathan/Source/choptuik-large-d-604
step b614 /home/nathan/Source/choptuik-large-d-614
echo "timing done $(date -u '+%H:%M')" > $OUT/timing_done.txt
