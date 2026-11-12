#!/bin/bash
# Runs inside a systemd scope. Logs the toolchain, hp/build.sh, its wall time and the scope's peak memory.
WT=/home/nathan/Source/choptuik-large-d-604
L=/home/nathan/Source/choptuik-large-d-raw/I604-dh370/build.log
cd "$WT" && . .venv/bin/activate
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH CC=clang CXX=clang++ CARGO_BUILD_JOBS=12
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
{
  echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC start; $(git rev-parse HEAD)"
  echo "# $(clang --version | head -1); $(rustc --version); $(maturin --version); cc -> $(command -v cc)"
  echo "# multidouble installed before: $(pip list 2>/dev/null | grep -ci '^multidouble ')"
} > "$L"
S=$(date +%s)
nice -n 10 hp/build.sh >> "$L" 2>&1
RC=$?
E=$(date +%s)
{
  echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end"
  echo "# build wall time: $((E-S)) s ($(( (E-S)/60 )) min)"
  echo "# scope memory.peak: $(cat $CG/memory.peak) bytes ($(( $(cat $CG/memory.peak)/1048576 )) MiB); swap.peak: $(cat $CG/memory.swap.peak 2>/dev/null) bytes"
  echo "exit $RC"
} >> "$L"
