#!/bin/bash
# #1021 diagnostic of b11-15's xi1 0.15 start solve (as boxes 7 and 16's, xi015d/*/diag/): the same hier_nb.py solve
# from the counted xi1 0.2 attempt's end state at verbose=2, at xi1 0.15 and 0.2, nice 19, 3600 s cap each.
#   diag_b1115p.sh      writes xi015d/b1115p/diag/
set -u
{ # read whole before it runs
. "$(dirname "$0")/common_z7.sh"
O=$D/xi015d/b1115p/diag; mkdir -p $O
read -r IA IW IB3 IC3 IB5 IC5 < $D/xi015d/b1115p/start02.txt || exit 1
cd $WT/solver/inner_stokes || exit 1
for XI in 0.15 0.2; do
  C="$PY -u hier_nb.py 5 $IA $IW --x=$IB3,$IC3,$IB5,$IC5 --fixA --schur --procs 1 --verbose=2 --xi1=$XI"
  echo "# $C (diagnostic, nice 19, $(stamp) UTC)" > $O/hier_nb_v2_xi$XI.log
  nice -n 19 timeout 3600 $C >> $O/hier_nb_v2_xi$XI.log 2>&1; echo "# exit $? $(stamp) UTC" >> $O/hier_nb_v2_xi$XI.log
done
exit
}
