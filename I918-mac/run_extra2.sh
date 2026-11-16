#!/bin/bash
# #918: after run_extra.sh, D 4 at eta inf and M 64: the third point of the gauge root's distance against M.
# The gauge root only: a determinant takes about 10 minutes at this size.
J=$(cd "$(dirname "$0")" && pwd)
# (run after run_extra.sh)
bash "$J/run_lam.sh" D4_etainf_M64 0 "--no_phys" sm_etainf_M64.npz
echo "$(date -u '+%F %T') UTC run_extra2 done" >> "$J/out/gate.log"
