#!/bin/bash
# Dry run of run_scan_r3.sh with a fake d18_secant.py (planted root ROOT), a fake raw repository that receives the two files after a delay, MAXP 2 (so the admission rule waits),
# and DRY=1 (no pins of the real worktree). usage: dryrun_r3.sh ROOT [BAD]   BAD=F|steps makes the fake record fail a bar.
# Exit 0 prints the DONE line and the results; this is a test of the driver's logic, not of the physics.
ROOT=${1:?planted root}; BAD=${2:-}
HERE=$(cd $(dirname $0)/.. && pwd)
T=$(mktemp -d /tmp/claude-1000/dryr3.XXXXXX); mkdir -p $T/out/in $T/wtm $T/raw
cp $HERE/run_scan_r3.sh $HERE/results_r3.py $HERE/scan_admit.sh $T/out/
cat > $T/out/in/read_lower.py <<'PYEOF'
import sys; print("fake read_lower", sys.argv[1:])
PYEOF
cat > $T/wtm/d18_secant.py <<'PYEOF'
import json, sys, time, os
a = [x for x in sys.argv[1:] if not x.startswith("--")]
mode = a[0]; root = float(os.environ["FAKE_ROOT"])
time.sleep(float(os.environ.get("FAKE_SLEEP", "4")))
if mode == "scan":
    lam = float(a[4]); out = a[5]
    print("D 23.0 k_c 127: |F| 1e-10 (record 1e-10), steps 11700 (record 11700): the record system", flush=True)
    print("block 12 by ellrs (avx2)", flush=True)
    d = root - lam
    rec = {"D": 23.0, "kc": 127, "lam": lam, "sign": 1.0 if d > 0 else -1.0, "ln": -4000.0 + 100 * abs(d), "noise": [1.0, 1.0], "dln": 1e-5, "noise_robust": True, "robust": True,
           "f64_sign": -1.0, "sec": 4, "sec_parts": [1, 2, 1], "b12": "rust", "role": "scan"}
    open(out, "a").write(json.dumps(rec) + "\n")
else:
    lo, hi, out = float(a[4]), float(a[5]), a[6]
    print("D 23.0 k_c 127: |F| 1e-10 (record 1e-10), steps 11700 (record 11700): the record system", flush=True)
    open(out, "a").write(json.dumps({"kind": "root", "status": "tol", "bracket": [root - 1.25e-5, root + 1.25e-5], "width": 2.5e-5, "signs": [1.0, -1.0], "robust": [True, True],
                                    "lam_lin": root, "lam_brent": root, "n_eval": 7}) + "\n")
PYEOF
cd $T/raw && git init -q -b main . && git config user.email t@t && git config user.name t && echo x > README && git add . && git commit -qm init
cd $T/out
F=1e-10; S=11700; [ "$BAD" = F ] && F=7e-10; [ "$BAD" = steps ] && S=12000
( sleep 12; cd $T/raw; mkdir -p I1101-mm5; python3 - <<PYEOF
import json
open("I1101-mm5/sol_l1kc127k025mm5_D23.0000.npy", "wb").write(b"fake state bytes\n")
open("I1101-mm5/l1kc127k025mm5.jsonl", "w").write(json.dumps({"F": $F, "steps": $S, "kappa": 0.25, "kc": 127, "D": 23.0, "u0": 0.04, "l": 1, "src": "l1kc127k050m3", "seconds": 1}) + "\n")
PYEOF
git add . && git commit -qm "mm5 files" ) &
export FAKE_ROOT=$ROOT DRY=1 OUT=$T/out WTM=$T/wtm SITE=/nonexistent RAWC=$T/raw REMOTE=main POLL=3 HOLD=3 MAXP=2 ADMIT_POLL=1 ADMIT_SETTLE=20 ADMIT_TICK=1
timeout 300 bash $T/out/run_scan_r3.sh; echo "driver exit $?"
cat $T/out/steps.txt | cut -c1-230; ls $T/out; cat $T/out/DONE_r3.txt $T/out/STOP_r3.txt 2>/dev/null; cat $T/out/results_r3_secant.md 2>/dev/null | tail -8
echo "dir $T"
