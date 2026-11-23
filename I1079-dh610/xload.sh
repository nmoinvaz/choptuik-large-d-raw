#!/bin/bash
# #1079 dh610, the cross-load of one excited zero: macm3's box and point files (in/macm3/, pinned blobs) through this machine's certify_M.py: krawczyk --point, controls --point, certify_M_recheck.py and its --mutate (the same commands as chain.sh).
# usage: bash xload.sh N
{
STAGE=xload; . $(dirname $0)/common.sh
pin_check
cd $W/solver/proof || exit 1
mkdir -p logs
for f in A_M_point_M3$T.json A_M_box_$BOX.json; do [ "$(git hash-object --no-filters $IN/$f)" = "$(grep " $f" $F/in/in_blobs_macm3.txt | cut -d' ' -f1)" ] || { stopmsg "$f is not the pinned blob"; exit 1; }; done
box=$IN/A_M_box_$BOX.json; pt=$IN/A_M_point_M3$T.json
run XL_krawczyk_pt_$BOX certify_M.py krawczyk --box=$box --point=$pt; k=$?
note "cross-load margins $BOX exit $k (0 wanted): $(head -1 logs/XL_krawczyk_pt_$BOX.log | cut -c1-200)"
run XL_controls_pt_$BOX certify_M.py controls --box=$box --point=$pt; c=$?
run XL_recheck_pt_$BOX certify_M_recheck.py $box; r=$?
run XL_recheck_pt_${BOX}_mutate certify_M_recheck.py $box --mutate; m=$?
note "cross-load: krawczyk exit $k, controls exit $c (0 wanted), recheck exit $r (0 wanted), recheck --mutate exit $m (1 wanted)"
[ $k = 0 ] && [ $c = 0 ] && [ $r = 0 ] && [ $m = 1 ] || { stopmsg "cross-load: krawczyk $k, controls $c, recheck $r, recheck --mutate $m"; exit 1; }
note "xload done"
exit 0
}
