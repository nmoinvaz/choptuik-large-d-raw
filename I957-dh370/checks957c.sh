#!/bin/bash
# #957 on dh370, after step 2 failed and the main-build control was stopped (dh610 reproduced the hook-line failure on plain
# main): the size of the planted-hook difference on the PR build (diff957.py), then the issue's steps 3 and 4 on the PR build
# (worktree choptuik-large-d-957), one at a time, 10 threads at nice 10. Steps 3 and 4 stop the chain at the first non-zero exit.
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I957-dh370
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
T=10
PR=/home/nathan/Source/choptuik-large-d-957
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
run() {   # run WT NAME CMD...: from WT/hp with WT's venv
  local wt=$1 name=$2; shift 2
  ( cd "$wt/hp" && . ../.venv/bin/activate || exit 1
    echo "== $name $(date -u '+%F %H:%M:%S') $(git -C "$wt" rev-parse --short HEAD) $*" > "$OUT/$name.log"
    echo "957 $name start $(date -u '+%F %T') $(git -C "$wt" rev-parse --short HEAD)" >> "$OUT/exits_957.txt"
    nice -n 10 "$@" >> "$OUT/$name.log" 2>&1
    rc=$?
    echo "exit $rc" >> "$OUT/$name.log"
    echo "957 $name exit $rc $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
    exit $rc )
}
run $PR diff_pr python3 "$OUT/diff957.py" "$RAW" "$ST" --threads $T --Np 6 --out "$OUT/diff_pr"
run $PR jbo_tangent1 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1" || exit 1
run $PR jbo_tangent1_D232 python3 jet_by_order_check.py "$RAW" "$ST2" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1_D232" || exit 1
run $PR jbo_tangent3 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 3 --out "$OUT/jbo_tangent3" || exit 1
echo "957 checks done $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
