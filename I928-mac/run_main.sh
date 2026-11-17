#!/bin/bash
# #928: after the pilot, the closures at D 11, then the chains from D 11.125 to 12 and from 12 to 13 at eta 0.3 and
# 1 with their rates, then M 24 and 48 at each coupling's last D. A coupling whose chain stops takes no further
# segment. One process at a time, 2 threads, nice 10.
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
log() { echo "$(date -u '+%F %T') UTC $*" >> "$OUT/runs.log"; }
# the closures: D 11 again from the secant through the chain's D 11.125 and 11.0625
for ETA in 0.3 1; do
    nice -n 10 $PY -u matter/sigma_ms/chain.py --M 32 --eta $ETA --out "$OUT" --threads 2 \
        --start "$OUT/sm_eta${ETA}_D11.0625_M32.npz" --start2 "$OUT/sm_eta${ETA}_D11.125_M32.npz" --Ds 11 \
        --extra "--solver band --it 40" > "$OUT/chain_eta${ETA}_closure.txt" 2>&1
    log "closure eta $ETA exit $?"
done
STOP03=0; STOP1=0
for SEG in "11.125 12" "12 13"; do
    set -- $SEG
    for ETA in 0.3 1; do
        if [ "$ETA" = "0.3" ] && [ $STOP03 -ne 0 ]; then continue; fi
        if [ "$ETA" = "1" ] && [ $STOP1 -ne 0 ]; then continue; fi
        read -r S1 S0 DL < <($PY "$J/last_two.py" "$OUT" $ETA $1)
        bash "$J/seg.sh" $ETA $1 $2 "$S1" "$S0" ""
        RC=$?
        if [ $RC -ne 0 ]; then
            log "the chain at eta $ETA stopped in the segment $1 to $2 (exit $RC)"
            if [ "$ETA" = "0.3" ]; then STOP03=1; else STOP1=1; fi
        fi
    done
done
# M 24 and 48 at each coupling's last D, by the recipe of #915, and their rates from the M 32 rate there
for ETA in 0.3 1; do
    read -r S1 S0 DL < <($PY "$J/last_two.py" "$OUT" $ETA 13)
    G=$($PY - "$OUT/sm_lam.jsonl" $ETA $DL <<'PY'
import json, sys
v = None
for l in open(sys.argv[1]):
    r = json.loads(l)
    if str(r["eta"]) == sys.argv[2] and float(r["D"]) == float(sys.argv[3]) and r["M"] == 32 and r.get("lam"):
        v = r["lam"]
print(v)
PY
)
    for M in 24 48; do
        T=eta${ETA}_D${DL}_M$M
        nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $ETA --D $DL --M $M --from "$S1" --out "$OUT" --tag $T \
            --solver band --threads 2 --it 40 > "$OUT/eta_$T.txt" 2>&1
        log "$T exit $?"
        nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $ETA --D $DL --M $M --from "$OUT/sm_$T.npz" --out "$OUT" \
            --tag eta${ETA}_D${DL}_polish_M$M --solver band --threads 2 --it 4 --tol 1e-30 > "$OUT/eta_${T}_polish.txt" 2>&1
        log "${T}_polish exit $?"
        nice -n 10 $PY matter/sigma_ms/mode_lam.py "$OUT/sm_eta${ETA}_D${DL}_polish_M$M.npz" --out "$OUT" --guess "$G" \
            --threads 2 --gauge_window 1e-12 --widths 1e-4,1e-3,1e-2 > "$OUT/lam_$T.txt" 2>&1
        log "lam $T exit $?"
    done
done
log "run_main done"
