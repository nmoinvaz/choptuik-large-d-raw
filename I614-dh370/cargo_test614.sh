#!/bin/bash
# hp's Rust tests on the 3c35f0c worktree, alone on the machine, in a scope without limits (for memory.peak).
WT=/home/nathan/Source/choptuik-large-d-614
L=/home/nathan/Source/choptuik-large-d-raw/I614-dh370/cargo_test.log
cd "$WT/hp" && . ../.venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH CC=clang CXX=clang++ RUSTFLAGS="-C target-cpu=native"
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC start: cargo test --release --lib (RUSTFLAGS=$RUSTFLAGS)" > "$L"
S=$(date +%s)
nice -n 10 cargo test --release --lib >> "$L" 2>&1
RC=$?
E=$(date +%s)
{ echo "# wall $((E-S)) s; scope memory.peak $(( $(cat $CG/memory.peak)/1048576 )) MiB"; echo "exit $RC"; } >> "$L"
