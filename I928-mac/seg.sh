#!/bin/bash
# #928: one segment of the kernel's chain in D at one coupling, M = 32, and the growth rates of its new states.
# One process, 2 threads, nice 10, no load gate. From the root of the checkout:
#   seg.sh <eta> <D_from> <D_to> <state at D_from> <state before it> <the two rates before, D:lam,D:lam>
J=$(cd "$(dirname "$0")" && pwd)
ETA=$1; A=$2; B=$3; S1=$4; S0=$5; PREV=$6
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
N=eta${ETA}_D${A}_${B}
echo "$(date -u '+%F %T') UTC chain $N start: load $(sysctl -n vm.loadavg | awk '{print $2}')" >> "$OUT/runs.log"
$PY -u matter/sigma_ms/chain.py --M 32 --eta $ETA --out "$OUT" --threads 2 --start "$S1" --start2 "$S0" \
    --D_from $A --D_to $B --dD 0.0625 --dD_max 0.0625 --extra "--solver band --it 40" --wrap "nice -n 10" \
    > "$OUT/chain_$N.txt" 2>&1
RC=$?
echo "$(date -u '+%F %T') UTC chain $N exit $RC" >> "$OUT/runs.log"
{ read -r P; read -r STATES; } < <($PY "$J/states_in.py" "$OUT" $ETA $A $B "$PREV")
if [ -n "$STATES" ]; then
    nice -n 10 $PY matter/sigma_ms/mode_lam.py $STATES --out "$OUT" --prev "$P" --threads 2 --gauge_window 1e-12 \
        --widths 1e-4,1e-3,1e-2,5e-2 > "$OUT/lam_$N.txt" 2>&1
    echo "$(date -u '+%F %T') UTC lam $N exit $?" >> "$OUT/runs.log"
fi
exit $RC
