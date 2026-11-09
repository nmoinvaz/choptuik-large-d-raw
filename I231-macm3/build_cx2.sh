#!/bin/bash
# I231-macm3: modecount_cx rebuilt on main 8bdb7937 (B = 5 added) while I241's three counts run. hp/modecount_build.sh ends with `cp lib build/modecount_cx<EXT>`, which writes into the
# module file those counts have loaded; this does its steps (the same cargo build, the same flags) but installs the result with a rename, so the running processes keep the old file.
cd ~/Source/choptuik-large-d/hp/modecount_cx
R=$(cd ../../../choptuik-large-d-raw/I231-macm3 && pwd)
source ~/Source/venv-macm3-314/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
date -u '+== %Y-%m-%d %H:%M:%S UTC modecount_cx build (venv-macm3-314, main 8bdb7937), install by rename' > $R/build_cx2.log
EXTRA="-C link-arg=-undefined -C link-arg=dynamic_lookup"
RUSTFLAGS="-C target-cpu=native $EXTRA" caffeinate -is nice -n 10 cargo build --release --offline >> $R/build_cx2.log 2>&1
echo "cargo build exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
EXT=$(python3 -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
shasum -a 256 build/modecount_cx$EXT > $R/modecount_cx_sha256_before.txt
cp target/release/libmodecount_cx.dylib build/modecount_cx.new
mv -f build/modecount_cx.new build/modecount_cx$EXT
shasum -a 256 build/modecount_cx$EXT > $R/modecount_cx_sha256_after.txt
python3 -c "import sys; sys.path.insert(0, 'build'); import modecount_cx; print('modecount_cx ok', modecount_cx.__file__)" >> $R/build_cx2.log 2>&1
echo "install by rename exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
