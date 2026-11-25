#!/bin/bash
# #1078 M' 160 (t5's amendment): root alone, then its own check (one sign change, the pivot ratio). Pins and environment as run_m160.sh.
{
O=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370/m160_root
WT=/home/nathan/Source/choptuik-large-d-1083
PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python
S=$O/in/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 HP_DENSE_M_MAX=160
unset HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $O/steps.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $O/STOP_$1.txt; step "STOP $1: $2"; echo "m160 CHAIN STOPPED at $1 $(stamp) UTC" > $O/DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $O || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 7c6177e1 ] && [ "$(blob $WT/hp/mode_matched.py)" = 3dd81b39 ] && [ "$(blob $S)" = 9ccd7a9e ] || stop 0 "worktree, mode_matched.py or state not pinned (7c6177e1, 3dd81b39, 9ccd7a9e)"
step "root alone starts (four skipped by order); 6 threads, nice 10, HP_DENSE_M_MAX=160, --lam0=6.3317279956 (load $(cut -d' ' -f1-3 /proc/loadavg))"
cd $WT/hp
t1=$(date +%s)
timeout 86400 nice -n 10 $PY -u mode_matched.py root $O/root_M160.jsonl $S --lam0=6.3317279956 --threads=6 > $O/root_M160.log 2>&1; rc=$?
step "root: exit $rc, $(( $(date +%s) - t1 )) s; $(grep 'root of D_m' $O/root_M160.log | tail -1 | cut -c1-200)"
echo "root $rc" >> $O/exit_codes.txt
grep -q '^Traceback' $O/root_M160.log && stop root "an exception (see root_M160.log)"
[ $rc = 124 ] && stop root "over 24 h"
bash $O/root_check.sh $O/root_M160.log > $O/root_check.txt 2>&1; crc=$?
step "root check: exit $crc (0 = one sign change and pivot ratio above 1e-20): $(tail -1 $O/root_check.txt | cut -c1-250)"
echo "m160 CHAIN DONE $(stamp) UTC" > $O/DONE.txt
step "chain done"
exit 0
}
