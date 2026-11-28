#!/bin/bash
# Dry run of run_scan1104.sh with a fake d18_secant.py (planted root ROOT), DRY=1 (no pins of the real worktree, no d18_secant selftests), MAXP 2 (the admission rule waits),
# and, if GATE=1, /tmp/dh170_prio_r3 present for 40 s (the driver must start nothing meanwhile; the real unit i1101r3 must be active for the gate to hold).
# usage: dryrun_scan1104.sh ROOT [GATE]    Exit 0 prints the steps and the DONE line; this tests the driver's logic, not the physics.
ROOT=${1:?planted root}; GATE=${2:-}
HERE=$(cd $(dirname $0)/.. && pwd)
T=$(mktemp -d /tmp/claude-1000/dryr1104.XXXXXX); mkdir -p $T/out/in $T/out/selftests $T/out/scan_050 $T/wtm
SCRIPT=${SCRIPT:-$HERE/run_scan1104.sh}
grep -q '"${OUT:=' $SCRIPT || { echo "refusing: $SCRIPT has no OUT override (it would run in the live folder)"; exit 9; }
cp $SCRIPT $T/out/run_scan1104.sh; cp $HERE/results_1104.py $HERE/scan_admit.sh $T/out/
cp -r $HERE/scan_070 $T/out/scan_070; cp $HERE/secant_070.jsonl $T/out/
cat > $T/out/in/read_lower.py <<'PYEOF'
import sys; print("fake read_lower", sys.argv[1:])
PYEOF
cat > $T/wtm/d18_secant.py <<'PYEOF'
import json, sys, time, os
a = [x for x in sys.argv[1:] if not x.startswith("--")]
mode = a[0]; root = float(os.environ["FAKE_ROOT"])
time.sleep(float(os.environ.get("FAKE_SLEEP", "4")))
print("D 23.125 k_c 127: |F| 1e-10 (record 1e-10), steps 5855 (record 5855): the record system", flush=True)
if mode == "scan":
    lam = float(a[4]); out = a[5]
    d = root - lam
    rec = {"D": 23.125, "kc": 127, "lam": lam, "sign": 1.0 if d > 0 else -1.0, "ln": -4000.0 + 100 * abs(d), "noise": [1.0, 1.0], "dln": 1e-5, "noise_robust": True, "robust": True,
           "f64_sign": -1.0, "sec": 4, "sec_parts": [1, 2, 1], "b12": "rust", "role": "scan"}
    open(out, "a").write(json.dumps(rec) + "\n")
else:
    out = a[6]
    open(out, "a").write(json.dumps({"kind": "root", "status": "tol", "bracket": [root - 1.25e-5, root + 1.25e-5], "width": 2.5e-5, "signs": [1.0, -1.0], "robust": [True, True],
                                    "lam_lin": root, "lam_brent": root, "n_eval": 7}) + "\n")
PYEOF
cd $T/out
echo "PASS fake" > DONE_resolve.txt
python3 - <<PYEOF
import json
open("l1kc127k050dh170d23125.jsonl", "w").write(json.dumps({"F": 1e-10, "steps": 5855, "kappa": 0.5, "kc": 127, "D": 23.125, "u0": 0.04, "l": 1}) + "\n")
open("sol_l1kc127k050dh170d23125_D23.1250.npy", "wb").write(b"fake state\n")
PYEOF
if [ -n "$GATE" ]; then touch /tmp/dh170_prio_r3; ( sleep 40; rm -f /tmp/dh170_prio_r3 ) & fi
export FAKE_ROOT=$ROOT DRY=1 OUT=$T/out WTM=$T/wtm WT=$T/wtm SITE=/nonexistent MAXP=2 ADMIT_POLL=1 ADMIT_SETTLE=20 ADMIT_TICK=1
timeout 600 bash $T/out/run_scan1104.sh; echo "driver exit $?"
cut -c1-220 $T/out/steps.txt | grep -E 'started|STOP|scan|secant|widen|done|record-system|results_1104' ; cat $T/out/DONE_scan050.txt $T/out/STOP_scan050.txt 2>/dev/null; tail -5 $T/out/results_1104_read.md 2>/dev/null | cut -c1-200
echo "dir $T"
