#!/bin/bash
# #918: a state at another M from an M = 32 state (the recipe of #915): run_eta.py --solver band from the resampled
# state, then one more run with --tol 1e-30. Usage: run_eta_M.sh <eta> <D> <M> <M 32 state file name>
J=$(cd "$(dirname "$0")" && pwd)
ETA=$1; D=$2; M=$3; SRC=$4
export PYTHONPATH=$J/site VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
PY=python3
T=eta${ETA}_D${D}_M$M
bash "$J/gate.sh" ${GATE:-100000} "$J/out/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $ETA --D $D --M $M \
    --from "$J/states/$SRC" --out "$J/out" --tag $T --solver band --threads 2 --it 40 > "$J/out/eta_$T.txt" 2>&1
echo "$(date -u '+%F %T') UTC $T exit $?" >> "$J/out/gate.log"
bash "$J/gate.sh" ${GATE:-100000} "$J/out/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $ETA --D $D --M $M \
    --from "$J/out/sm_$T.npz" --out "$J/out" --tag eta${ETA}_D${D}_polish_M$M --solver band --threads 2 --it 4 \
    --tol 1e-30 > "$J/out/eta_${T}_polish.txt" 2>&1
echo "$(date -u '+%F %T') UTC ${T}_polish exit $?" >> "$J/out/gate.log"
cp "$J/out/sm_eta${ETA}_D${D}_polish_M$M.npz" "$J/states/"
