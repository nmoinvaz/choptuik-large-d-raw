#!/bin/bash
# #1072 step 3 (t5's order, written before the run): waits for step 2 (unit i1072d) to end with STEP2_DONE.txt (L 0.9 at M' 128 passed its acceptance); a STOP_2*.txt or a dead
# unit without STEP2_DONE.txt ends this run too (step 3 does not run if step 2 fails). Then, unit i1072e, 6 threads, nice 10, worktree 1072b at ae96bcc6:
# 3b  L 0.4 at M' 128 from #1033's converged L 0.4 M' 160 state (raw I1033-dh610/states/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz, blob 9ccd7a9e, raw 55a49ace),
#     its own map kept (s0 1.9634954084936205 = the state's meta, L 0.4); a failure stops the run
# 3c  L 0.4 at M' 96 from the M' 128 state
# 3d  gp selftest: lowD_gamma.py --selftest <uniform D 3.15 M 128 state> <the D 3.044375 M' 128 state> (exit 0; part (1), the identity, runs on the D 3.15 state, part (2) the gp control on the mapped one)
# 3e  gamma at M' 128 and at M' 96, --lam0 = lam_guess(D of the state) --xtol=1e-11. Log: steps_step3.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
SRC1033=$RAWIN/I1033-dh610/states/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz
S128U=$RAWIN/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
WT=/home/nathan/Source/choptuik-large-d-1072b
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
ST=$OUT/states3; J=$OUT/solve_step3.jsonl; G=$OUT/gamma_D3.0444.jsonl
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step3.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_3$1.txt; step "STOP $1: $2"; exit 1; }
step "waiting for step 2 (unit i1072d) to end"
while [ ! -f $OUT/STEP2_DONE.txt ]; do
  ls $OUT/STOP_2*.txt $OUT/STOP_1d.txt > /dev/null 2>&1 && { step "step 2 stopped: $(cat $OUT/STOP_2*.txt 2>/dev/null | head -1 | cut -c1-200); step 3 does not run"; echo "NOT RUN: step 2 stopped" > $OUT/STEP3_NOT_RUN.txt; exit 1; }
  [ "$(systemctl --user is-active i1072d)" = active ] || [ -f $OUT/STEP2_DONE.txt ] || { step "unit i1072d ended without STEP2_DONE.txt; step 3 does not run"; echo "NOT RUN: i1072d ended without STEP2_DONE" > $OUT/STEP3_NOT_RUN.txt; exit 1; }
  sleep 30
done
step "step 2 done ($(cat $OUT/STEP2_DONE.txt)); step 3 starts; load $(cut -d' ' -f1-3 /proc/loadavg)"
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = ae96bcc6 ] || stop b "worktree not at ae96bcc6"
[ "$(git hash-object --no-filters $SRC1033 | cut -c1-8)" = 9ccd7a9e ] || stop b "the #1033 state is not blob 9ccd7a9e"
mkdir -p $ST $OUT/in3 && cp $SRC1033 $OUT/in3/
S0=$($PY -c "
import sys; sys.path.insert(0, '.')
from hpkernel.driver import load
z = load('$SRC1033'); print(repr(z[2]['map'][0]))" | tail -1)
LAM0=$($PY -c "
import sys; sys.path.insert(0, '.')
from hpkernel.driver import load
import lowD_gamma
D = load('$SRC1033')[2]['D']
print(repr(lowD_gamma.lam_guess(D)))" | tail -1)
step "the state: D 3.044375, M' 160, map s0 $S0 L 0.4; lam_guess(D of the state) = $LAM0 (gamma guess $(python3 -c "print(1/$LAM0)"))"
saved() { jq -r --argjson L $1 --argjson M $2 'select(.converged==true and .L==$L and .Mp==$M) | .saved' $J | tail -1; }
solve() {  # state L Mp
  t0=$(date +%s)
  nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $1 --pairs $2:$3 --s0 $S0 --states $ST --out $J --threads 6 >> $OUT/solve_step3.log 2>&1; rc=$?
  step "solve $(basename $1 .npz | cut -c1-70) -> L $2 M' $3: exit $rc, $(( $(date +%s) - t0 )) s"
  return $rc
}
solve $SRC1033 0.4 128 || stop b "L 0.4 at M' 128 from the M' 160 state did not converge"
P128=$(saved 0.4 128); [ -f "$P128" ] || stop b "no saved L 0.4 M' 128 state"
echo "STEP3B PASS $(stamp) UTC" > $OUT/STEP3B_DONE.txt
solve $P128 0.4 96 || stop c "L 0.4 at M' 96 from the M' 128 state did not converge"
P96=$(saved 0.4 96); [ -f "$P96" ] || stop c "no saved L 0.4 M' 96 state"
echo "STEP3C PASS $(stamp) UTC" > $OUT/STEP3C_DONE.txt
nice -n 10 $PY lowD_gamma.py --selftest $S128U $P128 --threads=6 > $OUT/selftest_gp_D3.0444_M128.txt 2>&1; g=$?
step "3d: lowD_gamma.py --selftest <uniform D 3.15 M 128> <D 3.044375 L 0.4 M' 128>: exit $g (0 wanted); $(tail -2 $OUT/selftest_gp_D3.0444_M128.txt | cut -c1-230 | tr '\n' '|')"
[ $g = 0 ] || stop d "the gp selftest exited $g"
echo "STEP3D PASS $(stamp) UTC" > $OUT/STEP3D_DONE.txt
gamma() {  # state label
  t0=$(date +%s)
  nice -n 10 timeout 21600 $PY -u lowD_gamma.py $G $1 --threads=6 --lam0=$LAM0 --xtol=1e-11 > $OUT/gamma_$2.log 2>&1; rc=$?
  step "3e gamma $2: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G | jq -c '{M,gamma,lam,F,n_signchanges,n_det,seconds}' | cut -c1-220)"
  return $rc
}
gamma $P128 D3.0444_M128 || stop e "gamma at M' 128 exited non-zero"
gamma $P96 D3.0444_M96 || stop e "gamma at M' 96 exited non-zero"
python3 -I - > $OUT/step3_summary.txt <<PYEOF
import json
r = {x["M"]: x for x in map(json.loads, open("$G"))}
a, b = r.get(128), r.get(96)
for M, x in sorted(r.items(), reverse=True):
    print(f"M' {M}: gamma {x['gamma']!r} lambda {x['lam']!r} |F| {x['F']:.2e} sign changes {x['n_signchanges']} determinants {x['n_det']} seconds {x['seconds']}")
if a and b and a.get("gamma") and b.get("gamma"):
    print(f"gamma(M' 128) - gamma(M' 96) = {a['gamma'] - b['gamma']:+.3e} (a resolution change, not a bound)")
PYEOF
echo "STEP3 DONE $(stamp) UTC" > $OUT/STEP3_DONE.txt
step "step 3 done: $(tr '\n' '|' < $OUT/step3_summary.txt | cut -c1-400)"
exit 0
}
