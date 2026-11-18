#!/bin/bash
# #957 on dh370: the remaining lines on the PR build (worktree choptuik-large-d-957, 954eadcb) with main 9bff3a1e's comparison
# (jet_by_order_check957.py, the coordinator's order): steps 3 and 4, then step 2 again (its default-path line failed under the old
# comparison on non-finite payload bits). One at a time, 10 threads at nice 10. Steps stop the chain at the first non-zero exit.
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I957-dh370
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
T=10
PR=/home/nathan/Source/choptuik-large-d-957
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
run() {   # run NAME CMD...: from the PR build's hp/ with its venv
  local name=$1; shift
  ( cd "$PR/hp" && . ../.venv/bin/activate || exit 1
    echo "== $name $(date -u '+%F %H:%M:%S') $(git -C "$PR" rev-parse --short HEAD) $*" > "$OUT/$name.log"
    echo "957 $name start $(date -u '+%F %T') $(git -C "$PR" rev-parse --short HEAD)" >> "$OUT/exits_957.txt"
    nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
    rc=$?
    echo "exit $rc" >> "$OUT/$name.log"
    echo "957 $name exit $rc $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
    exit $rc )
}
J=$OUT/jet_by_order_check957.py
run jbo_tangent1 python3 "$J" "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1" || exit 1
run jbo_tangent1_D232 python3 "$J" "$RAW" "$ST2" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1_D232" || exit 1
run jbo_tangent3 python3 "$J" "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 3 --out "$OUT/jbo_tangent3" || exit 1
run jbo_default2 python3 "$J" "$RAW" "$ST" --N 24 --threads $T --Np 6 --out "$OUT/jbo_default2" || exit 1
echo "957 checks done $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
