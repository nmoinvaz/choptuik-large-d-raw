#!/bin/bash
# #628, the M 160 part: gamma(3.5) at M 160 on lowD_gamma.py's path (the coordinator's message of 2026-11-13 01:12 UTC). From the root of the worktree
# ~/Source/choptuik-large-d-b596 at main b58895b; one run, 6 threads, nice 10, caffeinate.
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I628-macm3
caffeinate -is nice -n 10 python3 -u hp/lowD_gamma.py $R/lowD_gamma_D3.5_M160.jsonl hp/data/lowD_states/lowDmac15_D3.5000_M160.npz --threads=6 --polish=2 --lam0=3.1018757202 --xtol=1e-11 > $R/lowD_gamma_D3.5_M160.log 2>&1
echo "lowD_gamma M160 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
