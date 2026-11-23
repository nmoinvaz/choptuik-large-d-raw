#!/bin/bash
# #1078 after t5's change of plan (coordinator comment 7101701148): gamma at M' 96 with --hmax=0.025 --polish=4, then accept_step3.py. Unit i1078d, 6 threads, nice 10,
# worktree 1078 at main a4cd5eaa (lowD_gamma.py gains --hmax; Python only, no rebuild), HP_DENSE_M_MAX unset. Log: steps_hmax.txt. No hc from here.
#   plan_info.py: the plan's step counts at hmax 0.05 and 0.025 and the unpolished |F| on each; then
#   lowD_gamma.py gamma_D3.0444_M96_hmax0.025.jsonl <the M' 96 state> --threads=6 --hmax=0.025 --polish=4 --lam0=5.140867320755084 --xtol=1e-11
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1078
PY=$WT/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
G=$OUT/gamma_D3.0444_M96_hmax0.025.jsonl
G96=0.19451970603534682   # gamma(D 3.044375, L 0.4, M' 96) at hmax 0.05 of #1072 (raw I1072-dh370/gamma_D3.0444.jsonl, 12433a1d)
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_hmax.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_h$1.txt; step "STOP $1: $2"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = a4cd5eaa ] || stop 1 "worktree not at a4cd5eaa"
[ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob lowD_gamma.py)" = a05a336d ] && [ "$(blob $OUT/accept_step3.py)" = a056822b ] || stop 1 "the M' 96 state, lowD_gamma.py or accept_step3.py is not its pinned blob (6a0f83d2, a05a336d, a056822b)"
$PY -I $OUT/accept_step3.py selftest > $OUT/selftest_accept_step3_h.txt 2>&1; e0=$?
for m in sign F none_gamma; do $PY -I $OUT/accept_step3.py selftest --mutate=$m > /dev/null 2>&1; eval "e_$m=\$?"; done
step "start; accept_step3.py selftest exit $e0 (0 wanted), mutations sign $e_sign, F $e_F, none_gamma $e_none_gamma (1 wanted each); load $(cut -d' ' -f1-3 /proc/loadavg)"
[ $e0 = 0 ] && [ $e_sign = 1 ] && [ $e_F = 1 ] && [ $e_none_gamma = 1 ] || stop 1 "the checker's selftest or a control is not as required"
nice -n 10 $PY $OUT/plan_info.py $S96 0.025 6 > $OUT/plan_info.txt 2>&1; rp=$?
step "plan_info.py: exit $rp; $(grep -E '^hmax' $OUT/plan_info.txt | cut -c1-200 | tr '\n' '|')"
t0=$(date +%s)
nice -n 10 timeout 86400 $PY -u lowD_gamma.py $G $S96 --threads=6 --hmax=0.025 --polish=4 --lam0=5.140867320755084 --xtol=1e-11 > $OUT/gamma_D3.0444_M96_hmax0.025.log 2>&1; rc=$?
step "gamma at M' 96, hmax 0.025, polish 4: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G 2>/dev/null | jq -c '{M,gamma,lam,F,n_signchanges,n_det,hmax,seconds}' | cut -c1-240)"
[ $rc = 0 ] || stop 2 "gamma exited $rc"
$PY -I $OUT/accept_step3.py $G > $OUT/accept_step3_hmax.txt 2>&1; ra=$?
step "acceptance (accept_step3.py): exit $ra; $(grep -E 'PASS|FAIL' $OUT/accept_step3_hmax.txt | tr '\n' '|' | cut -c1-300)"
python3 -I - > $OUT/hmax_summary.txt <<PYEOF
import json
r = [json.loads(l) for l in open("$G")][-1]
g = r["gamma"]; g96 = $G96
d = g - g96
print(f"gamma(D 3.044375, L 0.4, M' 96, hmax 0.025, polish 4) = {g!r}, lambda {r['lam']!r}, |F| {r['F']:.2e}, sign changes {r['n_signchanges']}, {r['n_det']} determinants, {r['seconds']} s")
print(f"gamma(hmax 0.025) - gamma(hmax 0.05) = {d:+.3e} (the 0.05 value {g96!r}); reading written before the run: more than 1e-7: the plan is the lever; less than 1e-8: the plan is not the cause (the map, a second L, is next): {'MORE THAN 1e-7' if abs(d) > 1e-7 else 'LESS THAN 1e-8' if abs(d) < 1e-8 else 'BETWEEN 1e-8 AND 1e-7'}")
PYEOF
echo "HMAX DONE $(stamp) UTC (acceptance exit $ra)" > $OUT/HMAX_DONE.txt
exit 0
}
