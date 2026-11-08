#!/bin/bash
# I70 job 3 pre-step (macm3): rebuild hp/modecount_cx for Python 3.14 (the 3.13 build segfaults under 3.14), with the 3.14 venv active.
cd ~/Source/choptuik-large-d
J=$(cd ../choptuik-large-d-raw/I70-macm3/job3 && pwd)
source ~/Source/venv-macm3-314/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
date -u '+== %Y-%m-%d %H:%M:%S UTC bash hp/modecount_build.sh (venv-macm3-314)' > $J/build_cx.log
/usr/bin/time -l -o $J/build_cx_time.txt caffeinate -is nice -n 10 bash hp/modecount_build.sh >> $J/build_cx.log 2>&1
echo "modecount_build.sh exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $J/exits.txt
