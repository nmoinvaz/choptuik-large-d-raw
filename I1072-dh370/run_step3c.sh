#!/bin/bash
# #1072 step 3, t5's word: after the M' 128 gamma (unit i1072f) ends, rerun 3c with --it1 8 (same map and s0, resuming from its checkpoint), then gamma at M' 96
# (--lam0=5.1408197887863025 --xtol=1e-11); the acceptance as written (one sign change, |F| below 1e-27) by accept_step3.py (selftest and mutations first). Unit i1072g,
# 6 threads, nice 10, worktree 1072b at ae96bcc6. Log: steps_step3c.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
WT=/home/nathan/Source/choptuik-large-d-1072b
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
ST=$OUT/states3; J=$OUT/solve_step3.jsonl; G=$OUT/gamma_D3.0444.jsonl; LAM0=5.1408197887863025
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_step3c.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_3c$1.txt; step "STOP $1: $2"; exit 1; }
step "waiting for unit i1072f (the M' 128 gp selftest and gamma) to end"
while [ "$(systemctl --user is-active i1072f)" = active ]; do sleep 30; done
step "i1072f ended ($(ls $OUT/STEP3E_M128_DONE.txt $OUT/STOP_3b*.txt 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')); load $(cut -d' ' -f1-3 /proc/loadavg)"
cd $WT/hp || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = ae96bcc6 ] || stop a "worktree not at ae96bcc6"
$PY -I $OUT/accept_step3.py selftest > $OUT/selftest_accept_step3.txt 2>&1; e0=$?
for m in sign F none_gamma; do $PY -I $OUT/accept_step3.py selftest --mutate=$m > /dev/null 2>&1; eval "e_$m=\$?"; done
step "accept_step3.py selftest exit $e0 (0 wanted); mutations sign $e_sign, F $e_F, none_gamma $e_none_gamma (1 wanted each)"
[ $e0 = 0 ] && [ $e_sign = 1 ] && [ $e_F = 1 ] && [ $e_none_gamma = 1 ] || stop a "the checker's selftest or a control is not as required"
P128=$(jq -r 'select(.converged==true and .L==0.4 and .Mp==128) | .saved' $J | tail -1); [ -f "$P128" ] || stop a "no saved L 0.4 M' 128 state"
S0=$($PY -c "
import sys; sys.path.insert(0, '.')
from hpkernel.driver import load
print(repr(load('$P128')[2]['map'][0]))" | tail -1)
CK=$(ls $ST/*L0.4_M96_s1.9635_ckpt.npz 2>/dev/null | head -1)
step "3c rerun: L 0.4 at M' 96 from the M' 128 state, --it1 8, s0 $S0, checkpoint: $(basename "$CK" | cut -c1-60)"
t0=$(date +%s)
nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $P128 --pairs 0.4:96 --it1 8 --s0 $S0 --states $ST --out $J --threads 6 >> $OUT/solve_step3.log 2>&1; r=$?
step "3c rerun: exit $r, $(( $(date +%s) - t0 )) s"
P96=$(jq -r 'select(.converged==true and .L==0.4 and .Mp==96) | .saved' $J | tail -1)
[ $r = 0 ] && [ -f "$P96" ] || stop b "L 0.4 at M' 96 did not converge with --it1 8"
echo "STEP3C2 PASS $(stamp) UTC" > $OUT/STEP3C2_DONE.txt
t0=$(date +%s)
nice -n 10 timeout 21600 $PY -u lowD_gamma.py $G $P96 --threads=6 --lam0=$LAM0 --xtol=1e-11 > $OUT/gamma_D3.0444_M96.log 2>&1; rc=$?
step "3e gamma M' 96: exit $rc, $(( $(date +%s) - t0 )) s; $(tail -1 $G | jq -c '{M,gamma,lam,F,n_signchanges,n_det,seconds}' | cut -c1-230)"
[ $rc = 0 ] || stop c "gamma at M' 96 exited $rc"
$PY -I $OUT/accept_step3.py $G > $OUT/accept_step3.txt 2>&1; ra=$?
step "acceptance (accept_step3.py): exit $ra; $(grep -E 'PASS|FAIL|gamma\(M' $OUT/accept_step3.txt | tr '\n' '|' | cut -c1-500)"
echo "STEP3 FINAL DONE $(stamp) UTC (acceptance exit $ra)" > $OUT/STEP3_FINAL_DONE.txt
exit 0
}
