#!/bin/bash
# #1078 step 2 (unit i1078c, 6 threads, nice 10): gamma at D 3.044375 at M' 160 on the rebuilt kernel (c016b932), HP_DENSE_M_MAX=160:
#   lowD_gamma.py gamma_D3.0444_M160.jsonl <the M' 160 L 0.4 state, blob 9ccd7a9e> --threads=6 --lam0=5.140802680792423 --xtol=1e-11
# then accept_step3.py (its selftest and three mutations first, each mutation must exit 1) on the record, and the difference gamma(M' 160) - gamma(M' 128).
# A sampler logs the process RSS and MemAvailable every 60 s (a log; nothing is stopped or killed). Log: steps_step2.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S160=$RAWIN/I1072-dh370/in3/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz
G=$OUT/gamma_D3.0444_M160.jsonl
G128=0.19452215190758035   # gamma(D 3.044375, L 0.4, M' 128) of #1072 (raw I1072-dh370/gamma_D3.0444.jsonl, 12433a1d)
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step2.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_$1.txt; step "STOP $1: $2"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = c016b932 ] || stop 2 "worktree not at c016b932"
[ "$(blob $S160)" = 9ccd7a9e ] && [ "$(blob $OUT/accept_step3.py)" = a056822b ] || stop 2 "the M' 160 state or accept_step3.py is not its pinned blob (9ccd7a9e, a056822b)"
$PY -I $OUT/accept_step3.py selftest > $OUT/selftest_accept_step3.txt 2>&1; e0=$?
for m in sign F none_gamma; do $PY -I $OUT/accept_step3.py selftest --mutate=$m > /dev/null 2>&1; eval "e_$m=\$?"; done
step "start; accept_step3.py selftest exit $e0 (0 wanted), mutations sign $e_sign, F $e_F, none_gamma $e_none_gamma (1 wanted each); load $(cut -d' ' -f1-3 /proc/loadavg)"
[ $e0 = 0 ] && [ $e_sign = 1 ] && [ $e_F = 1 ] && [ $e_none_gamma = 1 ] || stop 2 "the checker's selftest or a control is not as required"
( echo "time,rss_kb,mem_available_kb" > $OUT/gamma_samples.csv
  while sleep 60; do
    echo "$(date -u +%T),$(ps -o rss= -p $(pgrep -f 'lowD_gamma.py .*gamma_D3.0444_M160' | tail -1) 2>/dev/null | tr -d ' '),$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" >> $OUT/gamma_samples.csv
  done ) &
SAMP=$!
t0=$(date +%s)
HP_DENSE_M_MAX=160 nice -n 10 timeout 172800 $PY -u lowD_gamma.py $G $S160 --threads=6 --lam0=5.140802680792423 --xtol=1e-11 > $OUT/gamma_D3.0444_M160.log 2>&1; rc=$?
kill $SAMP 2>/dev/null
step "gamma at M' 160: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G 2>/dev/null | jq -c '{M,gamma,lam,F,n_signchanges,n_det,seconds}' | cut -c1-230)"
[ $rc = 0 ] || stop 2 "gamma at M' 160 exited $rc"
$PY -I $OUT/accept_step3.py $G > $OUT/accept_step3.txt 2>&1; ra=$?
step "acceptance (accept_step3.py): exit $ra; $(grep -E 'PASS|FAIL' $OUT/accept_step3.txt | tr '\n' '|' | cut -c1-400)"
python3 -I - > $OUT/step2_summary.txt <<PYEOF
import json
r = [json.loads(l) for l in open("$G")][-1]
g = r["gamma"]; g128 = $G128
print(f"gamma(D 3.044375, L 0.4, M' 160) = {g!r}, lambda {r['lam']!r}, |F| {r['F']:.2e}, sign changes {r['n_signchanges']}, {r['n_det']} determinants, {r['seconds']} s")
print(f"gamma(M' 160) - gamma(M' 128) = {g - g128:+.3e} (beside the 96 to 128 change of +2.446e-6); bar 1e-8: {'at or below' if abs(g - g128) <= 1e-8 else 'above'}")
PYEOF
echo "STEP2 DONE $(stamp) UTC (acceptance exit $ra)" > $OUT/STEP2_DONE.txt
exit 0
}
