#!/bin/bash
# #685 on dh370: the 24-order octo-double series (anm_run.py --save_jet 2, #603's flags) at five of #603's states past D 251.9, one after the other, 12 threads, nice 10.
# Worktree choptuik-large-d-685 (main aedb403b) in the venv of choptuik-large-d-614 (the 3c35f0c build).
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I685-dh370
cd /home/nathan/Source/choptuik-large-d-685/hp && . /home/nathan/Source/choptuik-large-d-614/.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads 12 --corrector od --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3"
echo "hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__)'), main $(git rev-parse --short=8 HEAD)" > $R/exits_685.txt
for D in "$@"; do
  S=I603-win2/chain/anm_pin3_D$D.npz
  t=$(date +%s)
  echo "== D $D $(date -u '+%F %T') UTC" > $R/repro_D$D.log
  nice -n 10 python -u anm_run.py $RAW $R/repro --state $S --N 24 --tol_od 1e-60 $CH --save_jet 2 >> $R/repro_D$D.log 2>&1
  echo "D $D exit $? wall $(( $(date +%s) - t )) s $(date -u '+%F %T') UTC" >> $R/exits_685.txt
done
echo "all done $(date -u '+%F %T') UTC" >> $R/exits_685.txt
