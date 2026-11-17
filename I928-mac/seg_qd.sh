#!/bin/bash
# #928: one segment of the chain past the double-double stop, by the hand-over: the double-double band solver to
# 3e-27 (or to its stall, when that is at most 1e-24), then Newton in quad-double with the exact quad-double Jacobian,
# accepted by the rule of qd_protocol.md's addendum; the first point that is not accepted stops the chain
# (run_eta.py --qd --qd_accept). Then the growth rates of the new states. One process, 2 threads, nice 10.
#   seg_qd.sh <eta> <D_from> <D_to> <state at D_from> <state before it> <rates are taken for D above this>
J=$(cd "$(dirname "$0")" && pwd)
ETA=$1; A=$2; B=$3; S1=$4; S0=$5; LA=$6
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
N=eta${ETA}_D${A}_${B}_qd
echo "$(date -u '+%F %T') UTC chain $N start: load $(sysctl -n vm.loadavg | awk '{print $2}')" >> "$OUT/runs.log"
$PY -u matter/sigma_ms/chain.py --M 32 --eta $ETA --out "$OUT" --threads 2 --start "$S1" --start2 "$S0" \
    --D_from $A --D_to $B --dD 0.0625 --dD_max 0.0625 --dD_min 0.0625 --wrap "nice -n 10" \
    --extra "--solver band --it 40 --tol 3e-27 --handover_max 1e-24 --qd --qd_jac dd --qd_it 6 --qd_accept 1e-28" \
    > "$OUT/chain_$N.txt" 2>&1
RC=$?
echo "$(date -u '+%F %T') UTC chain $N exit $RC" >> "$OUT/runs.log"
{ read -r P; read -r STATES; } < <($PY "$J/states_in.py" "$OUT" $ETA $LA $B "")
if [ -n "$STATES" ]; then
    nice -n 10 $PY matter/sigma_ms/mode_lam.py $STATES --out "$OUT" --prev "$P" --threads 2 --gauge_window 1e-12 \
        --widths 1e-4,1e-3,1e-2,5e-2 > "$OUT/lam_$N.txt" 2>&1
    echo "$(date -u '+%F %T') UTC lam $N exit $?" >> "$OUT/runs.log"
fi
exit $RC
