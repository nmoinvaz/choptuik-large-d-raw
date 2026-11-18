#!/bin/bash
# #957 on dh370, after step 2 failed (the coordinator's order): the same default-path command on the main build of this machine
# (worktree choptuik-large-d-935, 808b1fac, multishoot 3.2.0), the planted-hook line's size on both builds (diff957.py), then
# the issue's steps 3 and 4 on the PR build (worktree choptuik-large-d-957). One at a time, 10 threads at nice 10. The main
# build's and the diff steps' exits do not stop the chain; steps 3 and 4 stop it at the first non-zero exit.
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I957-dh370
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz
T=10
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
MAIN=/home/nathan/Source/choptuik-large-d-935
PR=/home/nathan/Source/choptuik-large-d-957
run $MAIN jbo_default_main python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --out "$OUT/jbo_default_main"
run $MAIN diff_main python3 "$OUT/diff957.py" "$RAW" "$ST" --threads $T --Np 6 --out "$OUT/diff_main"
run $PR diff_pr python3 "$OUT/diff957.py" "$RAW" "$ST" --threads $T --Np 6 --out "$OUT/diff_pr"
run $PR jbo_tangent1 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1" || exit 1
run $PR jbo_tangent1_D232 python3 jet_by_order_check.py "$RAW" "$ST2" --N 24 --threads $T --Np 6 --tangent_from 1 --out "$OUT/jbo_tangent1_D232" || exit 1
run $PR jbo_tangent3 python3 jet_by_order_check.py "$RAW" "$ST" --N 24 --threads $T --Np 6 --tangent_from 3 --out "$OUT/jbo_tangent3" || exit 1
echo "957 checks done $(date -u '+%F %T')" >> "$OUT/exits_957.txt"
