#!/bin/bash
# #918: after run_full.sh, the x direction: the growth rate at D 10.5, eta 0.3 on #916's 27 nodes
J=$(cd "$(dirname "$0")" && pwd)
# (run after run_full.sh; its first run failed in plan_state.py and is in out/failed)
export PYTHONPATH=$J/site VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
nice -n 10 python3 "$J/plan_state.py" "$J/states/sm_eta0.3_D10.5_M32_nodes27_seed.npz" \
    "$J/states/sm_eta0.3_D10.5_M32_nodes27.npz" eta0.3_D10.5_M32_nodes27 > "$J/out/plan_nodes27.txt" 2>&1
python3 - "$J/out/sm_lam.jsonl" > "$J/out/guess_nodes27.txt" <<'PY'
import json, sys
v = None
for l in open(sys.argv[1]):
    r = json.loads(l)
    if str(r["eta"]) == "0.3" and r["D"] == 10.5 and r["M"] == 32 and r["K"] == 21 and r.get("lam"):
        v = r["lam"]
print(v)
PY
bash "$J/run_lam.sh" eta0.3_D10.5_nodes27 "$(cat "$J/out/guess_nodes27.txt")" "" sm_eta0.3_D10.5_M32_nodes27.npz
echo "$(date -u '+%F %T') UTC run_extra (second run) done" >> "$J/out/gate.log"
