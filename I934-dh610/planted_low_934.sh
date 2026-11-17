#!/bin/bash
# #934 (the coordinator's order after states.sh's planted failure at D 231): `octo_corrector.py planted` and its --mutate 10 control on
# #903's chain_k160 D 220 base, below the onset of the projection failure, under both builds: the 4.8.2 build (choptuik-large-d-934's venv)
# and the 4.8.0 python of #923's venv running the same hp code (as state_dump.py does, so nothing of #923's tree is written).
# 5 CPUs, nice 10, one run after another; logs planted220_{new,old}[_control].log.
taskset -cp 0-4 $$ > /dev/null
NEW=/home/nathan/Source/choptuik-large-d-934
OLD=/home/nathan/Source/choptuik-large-d-923
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I934-dh610
ST=/home/nathan/scratch934/states
P=I903-dh610/chain_k160/anm_pin3_D220.0000.npz
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
while ! grep -q '^exit [0-9]*$' $OUT/planted_480.log; do sleep 10; done
mkdir -p "$ST/$(dirname $P)" && git -C "$RAW" show "origin/main:$P" > "$ST/$P" || { echo "extract failed" > $OUT/planted220.log; exit 1; }
cd "$NEW/hp" || exit 1
run() { local tag=$1 py=$2; shift 2; echo "# $(date -u '+%F %T') UTC $tag: $py $*, load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/$tag.log; nice -n 10 "$py" -u octo_corrector.py planted "$ST" $P --threads 5 "$@" >> $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log; }
run planted220_new "$NEW/.venv/bin/python"
run planted220_new_control "$NEW/.venv/bin/python" --qd 0 --mutate 10
run planted220_old "$OLD/.venv/bin/python"
run planted220_old_control "$OLD/.venv/bin/python" --qd 0 --mutate 10
