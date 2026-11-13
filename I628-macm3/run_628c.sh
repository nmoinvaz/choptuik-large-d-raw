#!/bin/bash
# #628, dh370's half taken over by macm3 (the coordinator's message of 2026-11-13 06:02 UTC): the lowDvh family at M 96 (the control) and M 128, two runs at once,
# 3 threads each, nice 10, caffeinate. From the root of the worktree ~/Source/choptuik-large-d-b640 at main 9839474.
cd /Users/nathan/Source/choptuik-large-d-b640
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I628-macm3
for M in 96 128; do
  (caffeinate -is nice -n 10 python3 -u hp/lowD_gamma.py $R/lowD_gamma_D3.5_vh_M$M.jsonl hp/data/lowD_states/lowDvh_D3.5000_M$M.npz --threads=3 --polish=2 --lam0=3.1018757202 --xtol=1e-11 > $R/lowD_gamma_D3.5_vh_M$M.log 2>&1
   echo "lowD_gamma vh M$M exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
done
wait
