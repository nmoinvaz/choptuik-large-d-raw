#!/bin/bash
# #934 diagnostic (not one of the coordinator's scripts, run after states.sh's planted step raised StartNotProjected): the same
# `octo_corrector.py planted` on #903's D 231 state with the 4.8.0 kernel: the python of #923's venv (hpkernel and multidouble 4.8.0) running the
# NEW worktree's hp code (choptuik-large-d-934/hp), as states.sh's state_dump does, so nothing in #923's tree is touched. 5 CPUs, nice 10.
taskset -cp 0-4 $$ > /dev/null
NEW=/home/nathan/Source/choptuik-large-d-934
OLD=/home/nathan/Source/choptuik-large-d-923
OUT=/home/nathan/Source/choptuik-large-d-raw/I934-dh610
ST=/home/nathan/scratch934/states
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$NEW/hp" || exit 1
echo "# $(date -u '+%F %T') UTC planted with the 4.8.0 python ($OLD/.venv) on the 4.8.2 worktree's hp code" > $OUT/planted_480.log
nice -n 10 "$OLD/.venv/bin/python" -u octo_corrector.py planted "$ST" I903-dh610/chain_k160/anm_pin3_D231.0000.npz --threads 5 >> $OUT/planted_480.log 2>&1
echo "exit $?" >> $OUT/planted_480.log
