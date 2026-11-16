#!/bin/bash
# #918: the pilot's growth rates, D 9, 6 and 4 at eta 1 and D 4 at eta inf, each against sigdss's value.
# D 9 ran behind the gate of 31 (16:23 UTC). The others waited at it from 16:33 to 16:50 UTC with the load at 90 to
# 144, and run here without it, after the coordinator dropped the gate for #918's remaining runs.
J=$(cd "$(dirname "$0")" && pwd)
bash "$J/run_lam.sh" D6_eta1 3.806222 "" sm_eta1_D6_M32.npz
bash "$J/run_lam.sh" D4_eta1 8.648384 "" sm_eta1_M32.npz
bash "$J/run_lam.sh" D4_etainf 8.410420 "" sm_control_etainf_M32.npz
echo "$(date -u '+%F %T') UTC run_pilot done" >> "$J/out/gate.log"
