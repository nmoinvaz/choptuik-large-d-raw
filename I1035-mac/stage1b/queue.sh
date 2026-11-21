#!/bin/bash
{
# stage 1b curvature test (FACTORED_HORIZON 5.2), one process at a time at nice 10
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad
O=$S/i1035b/out
ST=$S/i1035/states
REF=$S/i1035/out
cd /Users/nathan/Source/choptuik-large-d-fh1b/hp
PY=/Users/nathan/venv-314/bin/python
D73=$ST/T81_conv_pin5_D73.0000_D73.000000.npz
D242=$ST/I461-win2_crawlJ_anm_pin3_D242.3642.npz
run() { name=$1; shift; echo "$(date -u '+%H:%M:%S') start $name" >> $O/queue.log; nice -n 10 $PY factored_horizon.py "$@" --out $O/$name.json > $O/$name.log 2>&1; rc=$?; echo "$(date -u '+%H:%M:%S') end $name exit $rc" >> $O/queue.log; }
run curvjac_D73 curvjac $D73 --prec 448 --cache $O/cache_D73.json
for m in D m1 m3; do run curv_D73_$m curv $D73 --prec 448 --cache $O/cache_D73.json --move $m; done
run curvjac_D242 curvjac $D242 --prec 448 --cache $O/cache_D242.json
for m in D m1 m3; do run curv_D242_$m curv $D242 --prec 448 --cache $O/cache_D242.json --move $m; done
run plant_D73 curv $D73 --prec 448 --cache $O/cache_D73.json --move D --plant $O/curv_D73_D.json
run plant_D242 curv $D242 --prec 448 --cache $O/cache_D242.json --move D --plant $O/curv_D242_D.json
for t in 1e-20 -1e-20 0; do run curvx_D242_$t curvx $D242 --prec 288 --ref $REF/ref_D242_288.json --t $t; done
run curvxq_D242 curvxq $O/curvx_D242_1e-20.json $O/curvx_D242_-1e-20.json $O/curvx_D242_0.json --t 1e-20 --curv $O/curv_D242_D.json
for t in 1e-20 -1e-20 0; do run curvx_D73_$t curvx $D73 --prec 288 --ref $REF/ref_D73_288.json --t $t; done
run curvxq_D73 curvxq $O/curvx_D73_1e-20.json $O/curvx_D73_-1e-20.json $O/curvx_D73_0.json --t 1e-20 --curv $O/curv_D73_D.json
echo "$(date -u '+%H:%M:%S') queue done" >> $O/queue.log
exit
}
