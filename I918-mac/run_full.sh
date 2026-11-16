#!/bin/bash
# #918: the growth rates from D 9 to 11. Waits for run_pilot.sh, then runs one mode_lam.py after another; every state
# starts behind the load gate. The order is the decision's: eta 0.3 first, then its other M, then eta 1, the scan,
# and the D 4 state at M 48 last.
J=$(cd "$(dirname "$0")" && pwd)
until grep -q 'run_pilot done' "$J/out/gate.log"; do /bin/sleep 30; done
# eta 0.3, M 32: the chain's states; the first guess is sigdss's rate at D 9
bash "$J/run_lam.sh" eta0.3_chain 3.175316 "" sm_eta0.3_D9_M32.npz sm_eta0.3_D9.5_M32.npz sm_eta0.3_D10_M32.npz \
    sm_eta0.3_D10.25_M32.npz sm_eta0.3_D10.5_M32.npz sm_eta0.3_D10.75_M32.npz sm_eta0.3_D11_polish_M32.npz
# the guess of a state at another M: the M 32 rate at its D, from the records
g() { python3 - "$J/out/sm_lam.jsonl" "$1" "$2" <<'PY'
import json, sys
v = None
for l in open(sys.argv[1]):
    r = json.loads(l)
    if str(r["eta"]) == sys.argv[2] and float(r["D"]) == float(sys.argv[3]) and r["M"] == 32 and r.get("lam"):
        v = r["lam"]
print(v)
PY
}
# eta 0.3 at M 24 and 48: D 10.5 (#915's states) and D 11 (made here)
bash "$J/run_lam.sh" eta0.3_D10.5_M24 "$(g 0.3 10.5)" "" sm_eta0.3_D10.5_polish_M24.npz
bash "$J/run_lam.sh" eta0.3_D10.5_M48 "$(g 0.3 10.5)" "" sm_eta0.3_D10.5_polish_M48.npz
bash "$J/run_eta_M.sh" 0.3 11 24 sm_eta0.3_D11_polish_M32.npz
bash "$J/run_lam.sh" eta0.3_D11_M24 "$(g 0.3 11)" "" sm_eta0.3_D11_polish_M24.npz
bash "$J/run_eta_M.sh" 0.3 11 48 sm_eta0.3_D11_polish_M32.npz
bash "$J/run_lam.sh" eta0.3_D11_M48 "$(g 0.3 11)" "" sm_eta0.3_D11_polish_M48.npz
# eta 1, M 32: #652's and #917's states (D 9 is the pilot's); the first guess is sigdss's rate at D 10
bash "$J/run_lam.sh" eta1_chain 2.919835 "" sm_eta1_D10_M32.npz sm_eta1_D10.475_M32.npz sm_eta1_D10.75_M32.npz \
    sm_eta1_D11_M32.npz
bash "$J/run_lam.sh" eta1_D10.475_M24 "$(g 1 10.475)" "" sm_eta1_D10.475_polish_M24.npz
bash "$J/run_lam.sh" eta1_D10.475_M48 "$(g 1 10.475)" "" sm_eta1_D10.475_polish_M48.npz
# the real roots of det M on 0.2 <= lambda <= 7 at D 11, eta 0.3
bash "$J/run_lam.sh" eta0.3_D11_scan 0 "--no_gauge --no_phys --scan 0.2,7,34" sm_eta0.3_D11_polish_M32.npz
# D 4 at M 48, eta inf: the tau resolution's part in the gauge root there
bash "$J/run_lam.sh" D4_etainf_M48 8.410420 "" sm_etainf_M48.npz
echo "$(date -u '+%F %T') UTC run_full done" >> "$J/out/gate.log"
