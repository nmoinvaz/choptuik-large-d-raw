#!/bin/bash
# #628, the coordinator's replacement of the M 160 run (message of 2026-11-13 01:15 UTC): the lowDhm layout family at M 96 and M 128, two runs at once,
# 3 threads each, nice 10, caffeinate. From the root of the worktree ~/Source/choptuik-large-d-b596 at main b58895b.
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I628-macm3
for M in 96 128; do
  (caffeinate -is nice -n 10 python3 -u hp/lowD_gamma.py $R/lowD_gamma_D3.5_hm_M$M.jsonl hp/data/lowD_states/lowDhm_D3.5000_M$M.npz --threads=3 --polish=2 --lam0=3.1018757202 --xtol=1e-11 > $R/lowD_gamma_D3.5_hm_M$M.log 2>&1
   echo "lowD_gamma hm M$M exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
done
wait
