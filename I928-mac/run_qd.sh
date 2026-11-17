#!/bin/bash
# #928: the continuation past the double-double stops, after the two checks of qd_protocol.md passed. Waits for
# run_main.sh's eta 1 segment and its rates, stops run_main.sh before its M 24 and 48 runs (they are taken at the
# chain's last D here instead), then runs eta 0.3 and eta 1 to D 13 by the hand-over, and M 24 and 48 at each
# coupling's last D the same way, with their rates.
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
log() { echo "$(date -u '+%F %T') UTC $*" >> "$OUT/runs.log"; }
until grep -q 'lam eta1_D12_13 exit\|run_main done' "$OUT/runs.log"; do /bin/sleep 5; done
pkill -f "bash $J/run_main.sh"
/bin/sleep 2
pkill -f 'matter/sigma_ms/run_eta.py --eta [0-9.]* --D [0-9.]* --M (24|48) '
log "run_main.sh stopped before its M 24 and 48 runs"
for ETA in 0.3 1; do
    # from the last double-double point on the grid of 0.0625
    read -r S1 S0 DL < <($PY - "$OUT/sm_records.jsonl" $ETA <<'PY'
import json, os, sys
out = os.path.dirname(sys.argv[1]); best = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    D = float(r["D"])
    if str(r["eta"]) == sys.argv[2] and r["converged"] and r["M"] == 32 and "qd" not in r and "polish" not in r["tag"] \
            and abs(D / 0.0625 - round(D / 0.0625)) < 1e-9:
        best[D] = r["tag"]
ds = sorted(best)[-2:]
print(os.path.join(out, f"sm_{best[ds[1]]}.npz"), os.path.join(out, f"sm_{best[ds[0]]}.npz"), "%.10g" % ds[1])
PY
)
    LA=$($PY -c "
import json
m = 0.0
for l in open('$OUT/sm_lam.jsonl'):
    r = json.loads(l)
    if str(r['eta']) == '$ETA' and r['M'] == 32 and r.get('lam'): m = max(m, float(r['D']))
print('%.10g' % m)")
    log "eta $ETA: quad-double hand-over from D $DL, rates above D $LA"
    bash "$J/seg_qd.sh" $ETA $DL 13 "$S1" "$S0" $LA
    log "eta $ETA: the hand-over chain's exit $?"
done
# M 24 and 48 at each coupling's last D, by the same hand-over, and their rates from the M 32 rate there
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
            --solver band --threads 2 --it 40 --tol 3e-27 --handover_max 1e-24 --qd --qd_jac dd --qd_it 6 --qd_accept 1e-28 \
            > "$OUT/eta_$T.txt" 2>&1
        log "$T exit $?"
        nice -n 10 $PY matter/sigma_ms/mode_lam.py "$OUT/sm_$T.npz" --out "$OUT" --guess "$G" --threads 2 \
            --gauge_window 1e-12 --widths 1e-4,1e-3,1e-2 > "$OUT/lam_$T.txt" 2>&1
        log "lam $T exit $?"
    done
done
log "run_qd done"
