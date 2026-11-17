#!/bin/bash
# #940 pilot on dh610: T84-mac's pin 5 and pin 7 states at D 68.5 through qd_window.py --mode full (the kernel of 4.5.0), pin 5 again at
# --plan_tol 1e-34, and pin 5 with --mutate dshift (the control), as four processes of 2 threads at nice 10.
WT=/home/nathan/Source/choptuik-large-d-940
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
echo "# $(date -u '+%F %T') UTC hp $(git rev-parse --short HEAD), hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/pilot.log
run() { local tag=$1; shift; (nice -n 10 $PY -u qd_window.py $OUT/$tag.jsonl "$@" --states $OUT/states_$tag --threads 2 > $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log) & }
run pin5_full $IN/T84-mac/pin5_D68.5000.npz --mode full
run pin7_full $IN/T84-mac/pin7_D68.5000.npz --mode full
run pin5_plan1e-34 $IN/T84-mac/pin5_D68.5000.npz --mode full --plan_tol 1e-34
run pin5_dshift $IN/T84-mac/pin5_D68.5000.npz --mode full --mutate dshift
wait
echo "# $(date -u '+%F %T') UTC pilot done" >> $OUT/pilot.log
