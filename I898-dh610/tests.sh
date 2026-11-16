#!/bin/bash
# #898: hp's octo-double Rust tests (prec_tests::od, ojet_lanes_bitwise among them), nice 10.
set -u
WT=/home/nathan/Source/choptuik-large-d-898
OUT=/home/nathan/Source/choptuik-large-d-raw/I898-dh610
L=$OUT/tests.log
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH RUSTFLAGS="-C target-cpu=native" CARGO_BUILD_JOBS=4
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC hp: cargo test --release --lib od:: -- --nocapture" > "$L"
S=$(date +%s); nice -n 10 cargo test --release --lib od:: -- --nocapture >> "$L" 2>&1; RC=$?
echo "# exit $RC, $(( $(date +%s) - S )) s, peak $(( $(cat "$CG/memory.peak") / 1048576 )) MiB" >> "$L"
echo "exit $RC" >> "$L"
exit $RC
