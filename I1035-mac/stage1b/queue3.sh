#!/bin/bash
{
# stage 1b: the amended plant at D 242.36 (FACTORED_HORIZON 5.2), after queue2.sh, one process at nice 10
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad
O=$S/i1035b/out
ST=$S/i1035/states
cd /Users/nathan/Source/choptuik-large-d-fh1b/hp
PY=/Users/nathan/venv-314/bin/python
D242=$ST/I461-win2_crawlJ_anm_pin3_D242.3642.npz
until grep -q "queue2 done" $O/queue.log; do sleep 20; done
run() { name=$1; shift; echo "$(date -u '+%H:%M:%S') start $name" >> $O/queue.log; nice -n 10 $PY factored_horizon.py "$@" --out $O/$name.json > $O/$name.log 2>&1; rc=$?; echo "$(date -u '+%H:%M:%S') end $name exit $rc" >> $O/queue.log; }
run plant_D242_c1e16 curv $D242 --prec 448 --cache $O/cache_D242.json --move D --plant $O/curv_D242_D.json --plant_c 1e16
echo "$(date -u '+%H:%M:%S') queue3 done" >> $O/queue.log
exit
}
