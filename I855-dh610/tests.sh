#!/bin/bash
# #855: hp's Rust tests, then modecount_cx's (the pivots of the complex LU and their control), nice 10.
set -u
WT=/home/nathan/Source/choptuik-large-d-855
OUT=/home/nathan/Source/choptuik-large-d-raw/I855-dh610
L=$OUT/tests.log
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH RUSTFLAGS="-C target-cpu=native" CARGO_BUILD_JOBS=4
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC hp: cargo test --release --lib" > "$L"
S=$(date +%s); nice -n 10 cargo test --release --lib >> "$L" 2>&1; RC1=$?
echo "# hp exit $RC1, $(( $(date +%s) - S )) s, peak $(( $(cat "$CG/memory.peak") / 1048576 )) MiB" >> "$L"
# modecount_cx's tests link libpython themselves: its pyo3 feature extension-module leaves Python's symbols to the
# interpreter that loads the module, and a test executable has none
PYLIB=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
PYVER=$(python -c "import sysconfig; print(sysconfig.get_config_var('LDVERSION'))")
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC modecount_cx: cargo test --release --offline (libpython$PYVER from $PYLIB)" >> "$L"
cd modecount_cx && S=$(date +%s)
RUSTFLAGS="-C target-cpu=native -L $PYLIB -l python$PYVER" LD_LIBRARY_PATH=$PYLIB nice -n 10 cargo test --release --offline >> "$L" 2>&1
RC2=$?
echo "# modecount_cx exit $RC2, $(( $(date +%s) - S )) s" >> "$L"
echo "exit $(( RC1 | RC2 ))" >> "$L"
