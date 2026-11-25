#!/bin/bash
# The probes of I1088-mac-a/probes, rerun with their output in this folder. Inputs: STATE (I966-dh370/ks_chain3b's
# anm_pin3_D245.5586.npz, raw origin/main), the code of wip/large-d-jump at CODE/hp, the kernel site at SITE.
# probe2.log and probe2_k13.log: python probe2.py STATE 2 STEP.npz [13] (kfreeze None, then 13); ladtest.log:
# python ladtest.py STATE 1e-8. These ran earlier the same way (2026-11-25 00:0x-00:2x UTC).
{
set -u
STATE=$1; CODE=$2; SITE=$3; HERE=$(cd "$(dirname "$0")" && pwd)
cd "$CODE/hp" || exit 1
export PYTHONPATH=$SITE OPENBLAS_NUM_THREADS=2
PY=/Users/nathan/venv-314/bin/python
date -u '+start %Y-%m-%d %H:%M:%S UTC'
nice -n 10 $PY -u "$HERE/ladtest2.py" "$STATE" > "$HERE/ladtest2.log" 2>&1
nice -n 10 $PY -u "$HERE/ladtest3.py" "$STATE" 1e-60,1e-52,1e-48 > "$HERE/ladtest3.log" 2>&1
nice -n 10 $PY -u "$HERE/ladtest4.py" "$STATE" 1e-44,1e-38,1e-30,1e-20 m > "$HERE/ladtest4.log" 2>&1
date -u '+end %Y-%m-%d %H:%M:%S UTC'
exit
}
