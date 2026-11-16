#!/bin/bash
# #918: the pilot's growth rates, D 9, 6 and 4 at eta 1 and D 4 at eta inf, each against sigdss's value
J=$(cd "$(dirname "$0")" && pwd)
bash "$J/run_lam.sh" D9_eta1 3.048509 "" sm_eta1_D9_M32.npz
bash "$J/run_lam.sh" D6_eta1 3.806222 "" sm_eta1_D6_M32.npz
bash "$J/run_lam.sh" D4_eta1 8.648384 "" sm_eta1_M32.npz
bash "$J/run_lam.sh" D4_etainf 8.410420 "" sm_control_etainf_M32.npz
echo "$(date -u '+%F %T') UTC run_pilot done" >> "$J/out/gate.log"
