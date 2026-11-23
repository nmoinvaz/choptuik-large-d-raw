#!/bin/bash
# #1078, t5's plan for feat/mode-equil a2607acb (hc 2026-11-23), unit i1078n, 6 threads, nice 10, one job on the machine. Stops at the first failed check (STOP_MEQUIL_<step>.txt).
# (1) HP_MODE_EQUIL unset, the new build against the c016b932 build of #1078 (same session, same inputs): mode_det at D 3.15 (L 0.7 M' 96 state, four lambdas)
#     bit for bit (mequil_compare.py bit); then lowD_gamma.py --selftest with lines equal to #1072's (blob 95b6ef1c).
# (2) the same four lambdas with HP_MODE_EQUIL=1 against unset: same sign and |d ln|det|| <= 1e-11 absolute (t5's ruling); the actual differences are printed.
# (3) D 3.044375 M' 96 state, HP_MODE_EQUIL=1: pivots at 5.140600; the pair 5.140819788786, 5.1408197887863025 resolved = same sign and ln|det| within 1e-6.
# (4) if (3) resolved: lowD_gamma.py --scan=5.14060,5.14100,21 with HP_MODE_EQUIL=1 (plan a: hmax 0.05, unpolished). Log: steps_mequil.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WTO=/home/nathan/Source/choptuik-large-d-1078      # c016b932 kernel (hpkernel .so sha256 b5098fcc...), python of 552a32d9 / 65ebf0c1
WTN=/home/nathan/Source/choptuik-large-d-1078m     # a2607acb
PYO=$WTO/.venv/bin/python; PYN=$WTN/.venv/bin/python
S315=$RAWIN/I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz
S128U=$RAWIN/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
S128M=$RAWIN/I1072-dh370/states3/tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635.npz
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
OLD=$RAWIN/I1072-dh370/selftest_gp_D3.0444_M128.txt
LAMS315="4.397684106690 4.397884106690 4.397786345516 4.397786345521"
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_mequil.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_MEQUIL_$1.txt; step "STOP $1: $2"; echo "MEQUIL CHECKS STOPPED at $1 $(stamp) UTC" > $OUT/MEQUIL_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $OUT || exit 9
[ "$(git -C $WTN rev-parse --short=8 HEAD)" = a2607acb ] || stop 0 "$WTN not at a2607acb"
[ "$(blob $S315)" = 9e683a14 ] && [ "$(blob $S128U)" = df2ab378 ] && [ "$(blob $S128M)" = 218460d9 ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $OLD)" = 95b6ef1c ] || stop 0 "an input is not its pinned blob (9e683a14, df2ab378, 218460d9, 6a0f83d2, 95b6ef1c)"
[ "$(blob $WTN/hp/lowD_gamma.py)" = e040c8a2 ] && [ "$(blob $WTO/hp/lowD_gamma.py)" = e040c8a2 ] || stop 0 "lowD_gamma.py is not blob e040c8a2 in both worktrees"
python3 mequil_compare.py selftest > selftest_mequil_compare.txt 2>&1 || stop 0 "mequil_compare.py selftest failed"
step "start; new kernel $($PYN -c 'import hpkernel; print(hpkernel.isa())') $(sha256sum $WTN/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so | cut -c1-16), old kernel $(sha256sum $WTO/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so | cut -c1-16); compare selftest: $(cat selftest_mequil_compare.txt | cut -c1-60)...; load $(cut -d' ' -f1-3 /proc/loadavg)"
# (1a) the old kernel's mode_det at D 3.15
t0=$(date +%s)
env -u HP_MODE_EQUIL nice -n 10 $PYO -u mequil_probe.py $WTO/hp probe_A_old_unset.jsonl $S315 $LAMS315 --threads=6 > probe_A_old_unset.log 2>&1 || stop 1a "probe A (old kernel) failed"
step "(1a) old kernel (c016b932), D 3.15 L 0.7 M' 96, four lambdas: $(( $(date +%s) - t0 )) s"
# (1b) the new kernel, HP_MODE_EQUIL unset: bit for bit
t0=$(date +%s)
env -u HP_MODE_EQUIL nice -n 10 $PYN -u mequil_probe.py $WTN/hp probe_B_new_unset.jsonl $S315 $LAMS315 --threads=6 > probe_B_new_unset.log 2>&1 || stop 1b "probe B (new kernel, unset) failed"
python3 mequil_compare.py bit probe_A_old_unset.jsonl probe_B_new_unset.jsonl > mequil_bit_AB.txt 2>&1; rc=$?
python3 - <<'PY'
import json, math
rows = [json.loads(l) for l in open("probe_B_new_unset.jsonl")]
rows[0]["ln"] = math.nextafter(rows[0]["ln"], math.inf); rows[0]["ln_hex"] = rows[0]["ln"].hex()
open("probe_B_mut_1ulp.jsonl", "w").write("".join(json.dumps(r) + "\n" for r in rows))
PY
python3 mequil_compare.py bit probe_A_old_unset.jsonl probe_B_mut_1ulp.jsonl > mequil_bit_AB_mutated.txt 2>&1; rcm=$?
step "(1b) new kernel unset against old, D 3.15: bit-identical check exit $rc (0 wanted), $(( $(date +%s) - t0 )) s; control (B with one ulp added to the first ln|det|) exit $rcm (1 wanted)"
[ $rc = 0 ] && [ $rcm = 1 ] || stop 1b "the unset kernel is not bit-identical to the old one, or its control did not fail"
# (2) HP_MODE_EQUIL=1 against unset
t0=$(date +%s)
HP_MODE_EQUIL=1 nice -n 10 $PYN -u mequil_probe.py $WTN/hp probe_C_new_equil.jsonl $S315 $LAMS315 --threads=6 > probe_C_new_equil.log 2>&1 || stop 2 "probe C (HP_MODE_EQUIL=1) failed"
python3 mequil_compare.py tol probe_B_new_unset.jsonl probe_C_new_equil.jsonl --abs=1e-11 > mequil_tol_BC.txt 2>&1; rc=$?
python3 - <<'PY'
import json
rows = [json.loads(l) for l in open("probe_C_new_equil.jsonl")]
rows[0]["ln"] += 1e-9
open("probe_C_mut_1e-9.jsonl", "w").write("".join(json.dumps(r) + "\n" for r in rows))
PY
python3 mequil_compare.py tol probe_B_new_unset.jsonl probe_C_mut_1e-9.jsonl --abs=1e-11 > mequil_tol_BC_mutated.txt 2>&1; rcm=$?
step "(2) D 3.15, HP_MODE_EQUIL=1 against unset: tol check exit $rc (0 wanted), $(( $(date +%s) - t0 )) s; control (C with 1e-9 added to the first ln|det|) exit $rcm (1 wanted); $(grep -o 'difference [^ ]*' mequil_tol_BC.txt | tr '\n' ' ')"
echo "MEQUIL STEP 2 rc $rc $(stamp) UTC" > MEQUIL_STEP2_DONE.txt
[ $rc = 0 ] && [ $rcm = 1 ] || stop 2 "the control at D 3.15 failed (HP_MODE_EQUIL=1 differs from unset by more than 1e-11, or its mutation did not fail)"
# (1c) the selftest, lines equal to #1072's
t0=$(date +%s)
( cd $WTN/hp && env -u HP_MODE_EQUIL nice -n 10 $PYN lowD_gamma.py --selftest $S128U $S128M --threads=6 > $OUT/selftest_gp_D3.0444_M128_mequil_unset.txt 2>&1 ); g=$?
if diff -q $OLD selftest_gp_D3.0444_M128_mequil_unset.txt > /dev/null; then same=EQUAL; else same=DIFFERENT; fi
diff $OLD selftest_gp_D3.0444_M128_mequil_unset.txt > selftest_diff_mequil_vs_1072.txt 2>&1
step "(1c) lowD_gamma.py --selftest on the new kernel, unset: exit $g (0 wanted), lines against #1072's: $same, $(( $(date +%s) - t0 )) s"
echo "MEQUIL STEP 1 rc $g $same $(stamp) UTC" > MEQUIL_STEP1_DONE.txt
[ $g = 0 ] && [ $same = EQUAL ] || stop 1c "the selftest exit $g, lines $same"
# (3) D 3.044375 M' 96 with HP_MODE_EQUIL=1
t0=$(date +%s)
HP_MODE_EQUIL=1 nice -n 10 $PYN -u mequil_probe.py $WTN/hp probe_E_d3044_equil.jsonl $S96 5.140600 5.140819788786 5.1408197887863025 --threads=6 > probe_E_d3044_equil.log 2>&1 || stop 3 "probe E (D 3.044375, HP_MODE_EQUIL=1) failed"
python3 mequil_compare.py resolved probe_E_d3044_equil.jsonl --pair=5.140819788786,5.1408197887863025 --abs=1e-6 > mequil_resolved_E.txt 2>&1; rc=$?
step "(3) D 3.044375 M' 96, HP_MODE_EQUIL=1: pair exit $rc (0 = resolved), $(( $(date +%s) - t0 )) s; $(cut -c1-200 probe_E_d3044_equil.log | tr '\n' '|')"
echo "MEQUIL STEP 3 rc $rc $(stamp) UTC" > MEQUIL_STEP3_DONE.txt
if [ $rc != 0 ]; then
  step "(3) not resolved: no scan (4)"
  echo "MEQUIL CHECKS DONE: step 3 not resolved $(stamp) UTC" > MEQUIL_DONE.txt
  exit 0
fi
# (4) the scan
step "(4) starts: HP_MODE_EQUIL=1 lowD_gamma.py scan_mequil.jsonl <M' 96 state> --threads=6 --scan=5.14060,5.14100,21 (plan a: hmax 0.05, state unpolished)"
t0=$(date +%s)
( cd $WTN/hp && HP_MODE_EQUIL=1 nice -n 10 timeout 172800 $PYN -u lowD_gamma.py $OUT/scan_mequil.jsonl $S96 --threads=6 --scan=5.14060,5.14100,21 > $OUT/scan_mequil.log 2>&1 ); rc=$?
step "(4) scan: exit $rc, $(( $(date +%s) - t0 )) s, $(grep -c '"scan": true' scan_mequil.jsonl 2>/dev/null) points"
echo "MEQUIL CHECKS DONE: scan exit $rc $(stamp) UTC" > MEQUIL_DONE.txt
exit 0
}
