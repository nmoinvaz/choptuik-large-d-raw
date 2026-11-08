#!/bin/bash
# I70 job 3, stage 1: the pilot (hp/modecount_lowD.py as in modecount_local.sh job 3), then the gate is read by hand.
cd ~/Source/choptuik-large-d
J=$(cd ../choptuik-large-d-raw/I70-macm3/job3 && pwd)
source ~/Source/venv-macm3-314/bin/activate
# the installed hpkernel finds the f64 solver (seed_from_f64) through $DSS_SOLVER_DIR, else a path of the cloud machine
export DSS_SOLVER_DIR=$HOME/Source/choptuik-large-d/solver
date -u '+pilot start %Y-%m-%d %H:%M:%S UTC' >> $J/driver.txt
date -u '+== %Y-%m-%d %H:%M:%S UTC python3 hp/modecount_lowD.py solver/data/neB_kc39_D4.0000.npy --kc=39 --M=32,48' > $J/pilot.log
caffeinate -is nice -n 10 python3 -u hp/modecount_lowD.py solver/data/neB_kc39_D4.0000.npy --kc=39 --M=32,48 >> $J/pilot.log 2>&1
echo "pilot exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $J/exits.txt
date -u '+pilot end %Y-%m-%d %H:%M:%S UTC' >> $J/driver.txt
