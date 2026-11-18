#!/bin/bash
# #957 on dh370: the issue's steps 1 to 4 on the build of PR #956's branch (worktree choptuik-large-d-957, its .venv), one at a
# time, 10 threads at nice 10, from hp/. R is the raw clone's push worktree. Stops at the first non-zero exit (a failure is
# a result, reported before anything else). Each step's log and JSON are in the raw folder, one line per step in exits_957.txt.
WT=/home/nathan/Source/choptuik-large-d-957
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I957-dh370
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
T=10
cd "$WT/hp" && . ../.venv/bin/activate || exit 1
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
# the low-memory recipe of the build (cargo test --release compiles the crate again)
export CARGO_BUILD_JOBS=6 CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
run() {
  local name=$1; shift
  echo "== $name $(date -u '+%F %H:%M:%S') $(git -C "$WT" rev-parse --short HEAD) $*" > "$OUT/$name.log"
  echo "957 $name start $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
  nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
  local rc=$?
  echo "exit $rc" >> "$OUT/$name.log"
  echo "957 $name exit $rc $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
  return $rc
}
run cargo_test_oseries cargo test --release --lib oseries_ -- --nocapture --test-threads=1 || exit 1
run jbo_default python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --out "$OUT/jbo_default" || exit 1
run jbo_tangent1 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1" || exit 1
run jbo_tangent1_D232 python3 jet_by_order_check.py "$RAW" "$ST2" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1_D232" || exit 1
run jbo_tangent3 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 3 --out "$OUT/jbo_tangent3" || exit 1
echo "957 checks done $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
