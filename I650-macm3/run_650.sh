#!/bin/bash
# #650: chain.py at M 64, resampled from each coupling's M 48 state (copied into data/ from I639-mac/data), the six couplings the M 64 run of #639 did not do.
# Worktree ~/Source/choptuik-large-d-b650 at origin/main fdcada23, the sigmams kernel built by build_sigma_ms.sh (FAST=1) into its matter/sigma_ms/site. 4 threads, nice 10, caffeinate.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I650-macm3
cd /Users/nathan/Source/choptuik-large-d-b650/matter/sigma_ms
export PYTHONPATH=$PWD/site
caffeinate -is nice -n 10 python3 -u chain.py --M 64 --resample_from 48 --etas 5,6,8.5,10,14,20 --out $R/data --threads 4 --extra "--jac mixed --jac_final mixed" > $R/chain_M64.log 2>&1
echo "chain M64 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt
