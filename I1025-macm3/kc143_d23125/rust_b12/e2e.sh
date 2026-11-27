#!/bin/bash
# #1025 macm3 kc143_d23125/rust_b12/e2e.sh (t5's order, hc 04:23 UTC 27 Nov, gate 3 of 4): ONE stored point of the k_c 143 D 23.0625 scan (lambda 0.015) re-evaluated with the branch's
# d18_secant.py scan --b12=rust --b12_threads=4 (worktree 1102m3 at d4b6b6ce, blob 9706e506) on the same state and stub with the same pins (a62d6f77, 548aa8b4).
# Beside the running secant of kc143_d230625, nice 15, 4 rayon threads, OPENBLAS/VECLIB 1 thread. Refused below 8 GiB available. RSS and memory sampled every 15 s. usage: bash e2e.sh
R=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3
H=$R/kc143_d23125/rust_b12; E=$H/e2e; IN=$R/kc87_leg_lambda/23.0625_kc143/in
WT=$HOME/Source/choptuik-large-d-1102m3; WTM=$WT/solver/matter; WTB=$HOME/Source/choptuik-large-d-1025m
PY=$HOME/Source/venv-macm3-1058b/bin/python
STATE=$IN/sol_l1kc143macm3d230625_D23.0625.npy; STUB=$IN/l1kc143macm3d230625.jsonl
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stamp() { date -u '+%F %T UTC'; }
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
mkdir -p $E; [ -z "$(ls $E 2>/dev/null)" ] || { echo "e2e/ is not empty"; exit 9; }
{
[ "$(git -C $WT rev-parse --short=8 HEAD)" = d4b6b6ce ] || { echo "worktree not at d4b6b6ce"; exit 9; }
[ "$(blob $WTM/d18_secant.py)" = 9706e506 ] || { echo "d18_secant.py is not blob 9706e506"; exit 9; }
[ "$(blob $STATE)" = a62d6f77 ] && [ "$(blob $STUB)" = 548aa8b4 ] || { echo "state or stub blob wrong"; exit 9; }
for f in dss_ell ell_ddm ell_dd ddnp; do [ "$(blob $WTM/$f.py)" = "$(blob $WTB/solver/matter/$f.py)" ] || { echo "$f.py differs from 505d8399's"; exit 9; }; done
AV=$(availgib); python3 -c "import sys; sys.exit(0 if $AV >= 8 else 1)" || { echo "only $AV GiB available"; exit 9; }
echo "$(stamp) e2e start: pins ok (worktree d4b6b6ce, d18_secant.py 9706e506, state a62d6f77, stub 548aa8b4, dss_ell/ell_ddm/ell_dd/ddnp equal 505d8399's); $AV GiB available; load $(sysctl -n vm.loadavg)"
cd $WTM
export PYTHONPATH=$HOME/Source/ellrs-site-1102m3 P4_WT_MATTER=$WTM OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
nice -n 15 $PY -u $R/kc143_d230625/in/capped_run.py 7200 $PY -u $WTM/d18_secant.py scan $STUB $STATE 23.0625 "0.015" $E/scan_D23.0625_rust.jsonl --pin=a62d6f77,548aa8b4 --b12=rust --b12_threads=4 > $E/scan_rust.log 2>&1 &
sp=$!
echo "time_utc,pid,rss_kB,pcpu,avail_GiB" > $E/samples.csv
while kill -0 $sp 2>/dev/null; do for p in $(pgrep -f "d18_secant.py scan.*rust_b12/e2e"); do echo "$(date -u '+%F %T'),$p,$(ps -o rss= -p $p | tr -d ' '),$(ps -o pcpu= -p $p | tr -d ' '),$(availgib)" >> $E/samples.csv; done; sleep 15; done
wait $sp; echo "$(stamp) e2e scan exit $?"
} >> $H/e2e_log.txt 2>&1
