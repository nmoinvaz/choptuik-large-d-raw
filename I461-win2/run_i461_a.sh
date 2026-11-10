#!/usr/bin/env bash
# #461 part A: the six short runs of hp/reseed.py checkq and truthq at 4 threads, one after the other, from the root of the worktree
# D:\choptuik-i446 (detached at d9e7f78), with venv-t126 (Python 3.12.8, hpkernel built 2026-11-05 22:51 local, multidouble f092018). Normal priority.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=D:/choptuik-large-d-raw
R=/d/choptuik-large-d-raw/I461-win2
cd /d/choptuik-i446 || exit 9
export PYTHONFAULTHANDLER=1
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
echo "part A start $(stamp)" >> $R/exits.txt
run() { name=$1; shift; t=$(date +%s); "$PY" -u hp/reseed.py "$@" --threads 4 > $R/A_$name.log 2>&1; rc=$?
        echo "A_$name exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $R/exits.txt; }
run 1_checkq_d6_D215.0              checkq $RAW/I215-win/chain_d6/pred_pin3_D215.0000.npz
run 2_checkq_d6_D215.0_sweeps1      checkq $RAW/I215-win/chain_d6/pred_pin3_D215.0000.npz --sweeps 1
run 3_checkq_d6_D209.0              checkq $RAW/I215-win/chain_d6/pred_pin3_D209.0000.npz
run 4_checkq_crawl_D215.0344        checkq $RAW/I19-win2/crawl/pred_pin3_D215.0344.npz
run 5_truthq_d6_D214.5              truthq $RAW/I215-win/chain_d6/anm_pin3_D214.5000.npz
run 6_truthq_d6_D214.5_sweeps1      truthq $RAW/I215-win/chain_d6/anm_pin3_D214.5000.npz --sweeps 1
echo "part A done $(stamp)" >> $R/exits.txt
