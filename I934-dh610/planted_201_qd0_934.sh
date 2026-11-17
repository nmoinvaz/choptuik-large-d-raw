#!/bin/bash
# #934 (the coordinator's order after the D 201 planted run's quad-double stage stalled, as expected near D 194): the octo-double stage is the pass criterion:
# `octo_corrector.py planted --qd 0` on #903's chain_k160 D 201 base under both builds, then its control `--qd 0 --mutate 10` under both, one run after another,
# 5 CPUs, nice 10. 4.8.2 = choptuik-large-d-934's venv; 4.8.0 = the python of #923's venv running the same hp code (as state_dump.py does). Logs planted201_{new,old}_qd0[_control].log.
taskset -cp 0-4 $$ > /dev/null
NEW=/home/nathan/Source/choptuik-large-d-934
OLD=/home/nathan/Source/choptuik-large-d-923
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
ST=/home/nathan/scratch934/states
P=I903-dh610/chain_k160/anm_pin3_D201.0000.npz
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$NEW/hp" || exit 1
run() { local tag=$1 py=$2; shift 2; echo "# $(date -u '+%F %T') UTC $tag: $py $*, load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/$tag.log; nice -n 10 "$py" -u octo_corrector.py planted "$ST" $P --threads 5 --qd 0 "$@" >> $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log; }
run planted201_new_qd0 "$NEW/.venv/bin/python"
run planted201_old_qd0 "$OLD/.venv/bin/python"
run planted201_new_qd0_control "$NEW/.venv/bin/python" --mutate 10
run planted201_old_qd0_control "$OLD/.venv/bin/python" --mutate 10
