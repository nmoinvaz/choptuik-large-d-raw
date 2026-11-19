#!/usr/bin/env bash
cd /Users/nathan/Source/choptuik-amp-trunc/solver/inner_amp
run() { n=$1; shift; timeout 7200 nice -n 10 /Users/nathan/venv-314/bin/python -u amp_flint_par.py 1.0 13 "$@" --out /Users/nathan/Source/choptuik-large-d-raw-i1016/I1016-mac/$n.json > /Users/nathan/Source/choptuik-large-d-raw-i1016/I1016-mac/$n.log 2>&1; echo "exit $?" >> /Users/nathan/Source/choptuik-large-d-raw-i1016/I1016-mac/$n.log; }
(run F_K13_J1000 1000 640 --procs 1 --fit phys --mf 6:12; run T5_K13_J1000 1000 640 --procs 1 --fit phys --mf 6:12 --trunc 5; run T5log_K13_J1000 1000 640 --procs 1 --fit phys --mf 6:12 --trunc 5 --fit-logs 1) &
(run F_K13_J1500 1500 640 --procs 1 --fit phys --mf 6:12; run T5_K13_J1500 1500 640 --procs 1 --fit phys --mf 6:12 --trunc 5; run T5log_K13_J1500 1500 640 --procs 1 --fit phys --mf 6:12 --trunc 5 --fit-logs 1) &
wait
echo done
