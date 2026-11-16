#!/bin/bash
# #916 part 2: the kernel's chain in D at eta = 0.3, M = 32, from #913's solution at D 10.5 down to D 9, back to 10.5
# by the secant (the closure), up to D 11, and three points at sigdss's own D. One process, 2 threads, nice 10, every
# run behind gate.sh (1-minute load below 31 at its start). From the root of the checkout:
#     run_chain.sh <output directory> <the D 10.5 state>
OUT=$1; START=$2
J=$(dirname "$0")
SITE=<site of #652>
PY=python3
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
WRAP="bash $J/gate.sh 31 $OUT/gate.log nice -n 10"
C="$PY -u matter/sigma_ms/chain.py --M 32 --eta 0.3 --out $OUT --threads 2"
X="--solver band --it 40"
st() { echo "$OUT/sm_eta0.3_D$1_M32.npz"; }
$C --start "$START" --D_from 10.5 --D_to 9 --dD 0.0625 --dD_max 0.0625 --extra "$X" --wrap "$WRAP" > "$OUT/chain_down.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_down exit $?" >> "$OUT/gate.log"
# the closure: D 10.5 again, from the secant through the chain's own D 10.375 and 10.4375
$WRAP $C --start "$(st 10.4375)" --start2 "$(st 10.375)" --Ds 10.5 --extra "$X" > "$OUT/chain_closure.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_closure exit $?" >> "$OUT/gate.log"
$C --start "$START" --start2 "$(st 10.4375)" --D_from 10.5 --D_to 11 --dD 0.0625 --dD_max 0.0625 --extra "$X" --wrap "$WRAP" > "$OUT/chain_up.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_up exit $?" >> "$OUT/gate.log"
# sigdss's own D values off the grid of 0.0625
$WRAP $C --start "$(st 10.4375)" --start2 "$(st 10.375)" --Ds 10.475 --extra "$X" > "$OUT/chain_x10.475.txt" 2>&1
$WRAP $C --start "$(st 10.125)" --start2 "$(st 10.1875)" --Ds 10.1 --extra "$X" > "$OUT/chain_x10.1.txt" 2>&1
$WRAP $C --start "$(st 9.75)" --start2 "$(st 9.8125)" --Ds 9.759375 --extra "$X" > "$OUT/chain_x9.759375.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_extras exit $?" >> "$OUT/gate.log"
