#!/bin/bash
# #958 on dh170: build D, hp at branch deps/multidouble-4.9.0 5b7cef1b (multidouble 4.9.0, multishoot 3.3.0, multisolver 0.1.1) in a fresh worktree and a fresh
# uv venv, the low-memory recipe (same bits as the default fat-LTO build). usage: bash build958.sh   (about 80 min, peak about 24 to 29 GB: nothing else heavy)
WT=/home/nathan/Source/choptuik-large-d-958
OUT=/home/nathan/Source/choptuik-large-d-raw/I958-dh170
cd "$WT" || exit 9
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$PATH
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=10
{ echo "# $(date -u '+%F %T') UTC build D, worktree $WT at $(git rev-parse HEAD), $(rustc --version), $(cargo --version), maturin $(maturin --version), python $(python --version 2>&1)"
  echo "# env: CARGO_PROFILE_RELEASE_LTO=$CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS=$CARGO_PROFILE_RELEASE_CODEGEN_UNITS CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS"
  echo "# raw clone stub read for the checks: ~/scratch958/raw at raw origin/main $(cat /home/nathan/scratch958/raw_commit.txt)"; } > $OUT/build.log
nice -n 15 /usr/bin/time -v bash hp/build.sh >> $OUT/build.log 2>&1
rc=$?
echo "# $(date -u '+%F %T') UTC build exit $rc" >> $OUT/build.log
# the crates the build resolved (Cargo.lock), and where hpkernel is
{ echo "## hp/Cargo.lock"; grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## hpkernel"; python -c 'import hpkernel,multidouble; print(hpkernel.__file__); print("isa", hpkernel.isa(), multidouble.isa())'
  so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
  echo "## crate strings in the .so"; strings -n 8 $so 2>/dev/null | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -20
  echo "## python multidouble"; cat .venv/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json; echo; } > $OUT/versions_D.txt 2>&1
exit $rc
