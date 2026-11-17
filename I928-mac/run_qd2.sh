#!/bin/bash
# #928: the continuation under the second addendum of qd_protocol.md (the first quad-double step may raise max |F|
# by less than a factor of 10). For each coupling: from its last accepted point to D 13 by the hand-over, with the
# rates of the new points; then M 24 and 48 at each coupling's last D the same way, with their rates.
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
log() { echo "$(date -u '+%F %T') UTC $*" >> "$OUT/runs.log"; }
lam_max() { $PY -c "
import json
m = 0.0
for l in open('$OUT/sm_lam.jsonl'):
    r = json.loads(l)
    if str(r['eta']) == '$1' and r['M'] == 32 and r.get('lam'): m = max(m, float(r['D']))
print('%.10g' % m)"; }
for ETA in 0.3 1; do
    if [ "$ETA" = "1" ]; then
        # eta 1 has no accepted hand-over point yet: from its last double-double point on the grid, D 12.3125
        S1=$OUT/sm_eta1_D12.3125_M32.npz; S0=$OUT/sm_eta1_D12.25_M32.npz; DL=12.3125
    else
        read -r S1 S0 DL < <($PY "$J/last_two.py" "$OUT" $ETA 13)
    fi
    LA=$(lam_max $ETA)
    log "eta $ETA: hand-over under the second addendum from D $DL, rates above D $LA"
    bash "$J/seg_qd.sh" $ETA $DL 13 "$S1" "$S0" $LA
    log "eta $ETA: the hand-over chain's exit $?"
done
for ETA in 0.3 1; do
    read -r S1 S0 DL < <($PY "$J/last_two.py" "$OUT" $ETA 13)
    G=$($PY -c "
import json
v = None
for l in open('$OUT/sm_lam.jsonl'):
    r = json.loads(l)
    if str(r['eta']) == '$ETA' and float(r['D']) == float('$DL') and r['M'] == 32 and r.get('lam'): v = r['lam']
print(v)")
    for M in 24 48; do
        T=eta${ETA}_D${DL}_M$M
        nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $ETA --D $DL --M $M --from "$S1" --out "$OUT" --tag $T \
            --solver band --threads 2 --it 40 --tol 3e-27 --handover_max 1e-24 --qd --qd_jac dd --qd_it 6 \
            --qd_accept 1e-28 --qd_first_rise 10 > "$OUT/eta_$T.txt" 2>&1
        log "$T exit $?"
        nice -n 10 $PY matter/sigma_ms/mode_lam.py "$OUT/sm_$T.npz" --out "$OUT" --guess "$G" --threads 2 \
            --gauge_window 1e-12 --widths 1e-4,1e-3,1e-2 > "$OUT/lam_$T.txt" 2>&1
        log "lam $T exit $?"
    done
done
log "run_qd2 done"
