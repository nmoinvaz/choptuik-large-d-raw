#!/bin/bash
{
# stage 1b controls that must fail (FACTORED_HORIZON 5.2), after queue.sh, one process at nice 10
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad
O=$S/i1035b/out
ST=$S/i1035/states
cd /Users/nathan/Source/choptuik-large-d-fh1b/hp
PY=/Users/nathan/venv-314/bin/python
D73=$ST/T81_conv_pin5_D73.0000_D73.000000.npz
until grep -q "queue done" $O/queue.log; do sleep 20; done
run() { name=$1; shift; echo "$(date -u '+%H:%M:%S') start $name" >> $O/queue.log; nice -n 10 $PY factored_horizon.py "$@" --out $O/$name.json > $O/$name.log 2>&1; rc=$?; echo "$(date -u '+%H:%M:%S') end $name exit $rc" >> $O/queue.log; }
run mut_r0_D73 curv $D73 --prec 448 --cache $O/cache_D73.json --move D --mutate=r0
run mut_plant1_D73 curv $D73 --prec 448 --cache $O/cache_D73.json --move D --plant $O/curv_D73_D.json --mutate=plant1
echo "$(date -u '+%H:%M:%S') queue2 done" >> $O/queue.log
exit
}
