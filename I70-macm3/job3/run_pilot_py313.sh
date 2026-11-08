#!/bin/bash
# I70 job 3, control of the pilot: the same modecount_lowD.py command on Python 3.13 (venv-macm3), the state written to this folder instead of hp/data.
cd ~/Source/choptuik-large-d
J=$(cd ../choptuik-large-d-raw/I70-macm3/job3 && pwd)
source ~/Source/venv-macm3/bin/activate
export DSS_SOLVER_DIR=$HOME/Source/choptuik-large-d/solver
date -u '+== %Y-%m-%d %H:%M:%S UTC (venv-macm3, Python 3.13.3) python3 hp/modecount_lowD.py solver/data/neB_kc39_D4.0000.npy --kc=39 --M=32,48 --out=<this folder>/state_D4.0000_M48_py313.npz' > $J/pilot_py313.log
caffeinate -is nice -n 10 python3 -u hp/modecount_lowD.py solver/data/neB_kc39_D4.0000.npy --kc=39 --M=32,48 --out=$J/state_D4.0000_M48_py313.npz >> $J/pilot_py313.log 2>&1
echo "pilot on 3.13 exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $J/exits.txt
