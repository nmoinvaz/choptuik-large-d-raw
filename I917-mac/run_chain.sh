#!/bin/bash
# #917: the kernel's chain in D at eta = 1, M = 32, past the end of #652's chain: from its D 10.475 state to D 10.5,
# then in steps of 0.0625 to D 11; D 10.475 again from the secant through the chain's D 10.5625 and 10.5 (the
# closure); and three points at sigdss's own D. One process, 2 threads, nice 10, every run behind gate.sh (1-minute
# load below 31 at its start). From the root of the checkout: run_chain.sh <output directory> <seed directory>
OUT=$1; SEEDS=$2
J=$(dirname "$0")
SITE=<site of #652>
PY=python3
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
WRAP="bash $J/gate.sh 31 $OUT/gate.log nice -n 10"
C="$PY -u matter/sigma_ms/chain.py --M 32 --eta 1 --out $OUT --threads 2"
X="--solver band --it 40"
st() { echo "$OUT/sm_eta1_D$1_M32.npz"; }
sd() { echo "$SEEDS/sm_eta1_D$1_M32.npz"; }
$WRAP $C --start "$(sd 10.475)" --start2 "$(sd 10.4375)" --Ds 10.5 --extra "$X" > "$OUT/chain_first.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_first exit $?" >> "$OUT/gate.log"
$C --start "$(st 10.5)" --start2 "$(sd 10.475)" --D_from 10.5 --D_to 11 --dD 0.0625 --dD_max 0.0625 --extra "$X" --wrap "$WRAP" > "$OUT/chain_up.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_up exit $?" >> "$OUT/gate.log"
$WRAP $C --start "$(st 10.5)" --start2 "$(st 10.5625)" --Ds 10.475 --extra "$X" > "$OUT/chain_closure.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_closure exit $?" >> "$OUT/gate.log"
$WRAP $C --start "$(sd 10.125)" --start2 "$(sd 10.0625)" --Ds 10.1 --extra "$X" > "$OUT/chain_x10.1.txt" 2>&1
$WRAP $C --start "$(sd 10.375)" --start2 "$(sd 10.4375)" --Ds 10.3796875 --extra "$X" > "$OUT/chain_x10.3796875.txt" 2>&1
$WRAP $C --start "$(sd 10.475)" --start2 "$(sd 10.4375)" --Ds 10.474609375 --extra "$X" > "$OUT/chain_x10.474609375.txt" 2>&1
echo "$(date -u '+%F %T') UTC chain_extras exit $?" >> "$OUT/gate.log"
