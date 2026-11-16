#!/bin/bash
# #903 on dh170 (the coordinator's command of 2026-11-16): p150_200, the order-150 base polish of T138's D 200 state,
# then, if it converges to max|F| <= 1e-60, chain_k150 from that base toward the fold. 8 threads, nice 10. Python and
# hp/data from a worktree of main at 7f88c5bb (no hp/ change since 5897ee28); hpkernel from the checkout's venv (#920).
SRC=/home/nathan/Source/choptuik-large-d
WT=/home/nathan/Source/choptuik-large-d-903
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I903-dh170
PY=$SRC/.venv/bin/python
S=T138-win2/chain_o/anm_pin3_D200.0000.npz
B=I903-dh170/p150_200/base_pin3_D200.0000.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --D_max 262 --threads 8 --corrector od
 --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1
 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
log() { echo "903 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_903.txt; }
[ -s $RAW/$S ] || { log "missing $S"; exit 9; }
cd $WT/hp || exit 9
export PYTHONFAULTHANDLER=1
log "start p150_200, hp $(git rev-parse --short=8 HEAD), hpkernel $($PY -c 'import hpkernel; print(hpkernel.__file__)' 2>/dev/null), load $(cut -d' ' -f1-3 /proc/loadavg)"
t=$(date +%s)
nice -n 10 $PY -u anm_run.py $RAW $OUT/p150_200 --state $S $F --ks 150 --keep_plan 0 --steps 0 --save_base 1 \
  >> $OUT/p150_200.log 2>&1
rc=$?
log "p150_200 exit $rc wall $(( $(date +%s) - t )) s"
[ $rc -eq 0 ] || exit $rc
# gate: the last octo-double Newton line must read converged with max|F| <= 1e-60, and the base must be saved
gate=$($PY -I - $OUT/p150_200.log $RAW/$B <<'EOF'
import os, re, sys
last = None
for line in open(sys.argv[1], errors="replace"):
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (converged|not converged)", line)
    if m:
        last = m
ok = last is not None and last.group(3) == "converged" and float(last.group(2)) <= 1e-60 and os.path.getsize(sys.argv[2]) > 0
print("pass" if ok else "fail", last.group(0) if last else "no octo-double Newton line")
EOF
)
log "gate: $gate"
case "$gate" in pass*) ;; *) exit 8 ;; esac
t=$(date +%s)
nice -n 10 $PY -u anm_run.py $RAW $OUT/chain_k150 --state $B $F --ks 150 --keep_plan 1 --steps 400 \
  >> $OUT/chain_k150.log 2>&1
rc=$?
log "chain_k150 exit $rc wall $(( $(date +%s) - t )) s"
exit $rc
