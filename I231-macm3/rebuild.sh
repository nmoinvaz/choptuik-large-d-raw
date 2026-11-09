#!/bin/bash
# I231-macm3: the rebuild after "hp: accept M = 40 in the solver binding" (1bad14fd), venv-macm3-314, LTO off and 16 codegen units (24 GB).
cd ~/Source/choptuik-large-d
R=$(cd ../choptuik-large-d-raw/I231-macm3 && pwd)
source ~/Source/venv-macm3-314/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
date -u '+rebuild start %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
pip freeze > $R/freeze_before_rebuild.txt
date -u '+== %Y-%m-%d %H:%M:%S UTC bash hp/build.sh (venv-macm3-314, main 1bad14fd)' > $R/build.log
/usr/bin/time -l -o $R/build_time.txt caffeinate -is nice -n 10 bash hp/build.sh >> $R/build.log 2>&1
echo "hp/build.sh exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
pip freeze > $R/freeze_after_rebuild.txt
date -u '+== %Y-%m-%d %H:%M:%S UTC bash hp/modecount_build.sh (venv-macm3-314)' > $R/build_cx.log
caffeinate -is nice -n 10 bash hp/modecount_build.sh >> $R/build_cx.log 2>&1
echo "hp/modecount_build.sh exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
date -u '+rebuild end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
