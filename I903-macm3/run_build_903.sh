#!/bin/bash
# macm3b: hp/build.sh at origin/main into venv-macm3-main, with the low-memory recipe of AGENTS.md (LTO off, 16 codegen units)
R=$HOME/Source/choptuik-large-d-raw-903/I903-macm3
P=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/c5600845-6df1-47e0-a462-0d9c5c618a7b/scratchpad
source $HOME/Source/venv-macm3-main/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
cd $HOME/Source/choptuik-large-d-903/hp
echo "903 build start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse --short=8 HEAD) rustc $(rustc --version) LTO=false CGU=16" >> $R/build_times.txt
caffeinate -is nice -n 10 bash ./build.sh > $R/build.log 2>&1 &
BP=$!
/Users/nathan/Source/venv-macm3-314/bin/python3 $P/mem_monitor.py $BP $R/build_mem.csv &
MP=$!
wait $BP
rc=$?
wait $MP
echo "903 build exit $rc $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/build_times.txt
