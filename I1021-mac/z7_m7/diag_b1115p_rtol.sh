#!/bin/bash
# #1021 diagnostic of b11-15's start solve: diag_b1115p.sh's solves with the integrator tolerance INNER_NB_RTOL 1e-14
# (default 1e-12), at xi1 0.15 and 0.2, nice 19, 3600 s cap each. Writes xi015d/b1115p/diag/*_rtol1e-14.log
set -u
{ # read whole before it runs
. "$(dirname "$0")/common_z7.sh"
O=$D/xi015d/b1115p/diag
read -r IA IW IB3 IC3 IB5 IC5 < $D/xi015d/b1115p/start02.txt || exit 1
cd $WT/solver/inner_stokes || exit 1
for XI in 0.15 0.2; do
  C="$PY -u hier_nb.py 5 $IA $IW --x=$IB3,$IC3,$IB5,$IC5 --fixA --schur --procs 1 --verbose=2 --xi1=$XI"
  echo "# INNER_NB_RTOL=1e-14 $C (diagnostic, nice 19, $(stamp) UTC)" > $O/hier_nb_v2_xi${XI}_rtol1e-14.log
  INNER_NB_RTOL=1e-14 nice -n 19 timeout 3600 $C >> $O/hier_nb_v2_xi${XI}_rtol1e-14.log 2>&1
  echo "# exit $? $(stamp) UTC" >> $O/hier_nb_v2_xi${XI}_rtol1e-14.log
done
exit
}
