#!/bin/bash
# #934 (the coordinator's order, the multi session approving D 201): `octo_corrector.py planted` and its --mutate 10 control on #903's chain_k160 D 201 base
# (p_min 1.3e-8, the base nearest the chain's start) under both builds: 4.8.2 (choptuik-large-d-934's venv) and the 4.8.0 python of #923's venv running the same
# hp code (as state_dump.py does). 5 CPUs, nice 10, one run after another; logs planted201_{new,old}[_control].log. If D 201 fails under both alike, stop and report.
taskset -cp 0-4 $$ > /dev/null
NEW=/home/nathan/Source/choptuik-large-d-934
OLD=/home/nathan/Source/choptuik-large-d-923
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
ST=/home/nathan/scratch934/states
P=I903-dh610/chain_k160/anm_pin3_D201.0000.npz
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p "$ST/$(dirname $P)" && git -C "$RAW" show "origin/main:$P" > "$ST/$P" || { echo "extract failed" > $OUT/planted201.log; exit 1; }
cd "$NEW/hp" || exit 1
run() { local tag=$1 py=$2; shift 2; echo "# $(date -u '+%F %T') UTC $tag: $py $*, load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/$tag.log; nice -n 10 "$py" -u octo_corrector.py planted "$ST" $P --threads 5 "$@" >> $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log; }
run planted201_new "$NEW/.venv/bin/python"
run planted201_new_control "$NEW/.venv/bin/python" --qd 0 --mutate 10
run planted201_old "$OLD/.venv/bin/python"
run planted201_old_control "$OLD/.venv/bin/python" --qd 0 --mutate 10
