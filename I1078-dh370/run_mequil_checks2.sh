#!/bin/bash
# #1078, t5's plan for feat/mode-equil a2607acb (hc 2026-11-23), second part after (1a), (1b) and (2) passed (run_mequil_checks.sh, unit i1078n, stopped by t5's reorder 18:22 UTC while (1c) was 40 s old), unit i1078o, 6 threads, nice 10, one job on the machine. Order now (3), (4) if resolved, then (1c). Stops at the first failed check (STOP_MEQUIL_<step>.txt).
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
step "part 2 starts (t5's reorder: (3), (4) if resolved, then (1c) the selftest); new kernel $($PYN -c 'import hpkernel; print(hpkernel.isa())') $(sha256sum $WTN/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so | cut -c1-16), old kernel $(sha256sum $WTO/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so | cut -c1-16); compare selftest: $(cat selftest_mequil_compare.txt | cut -c1-60)...; load $(cut -d' ' -f1-3 /proc/loadavg)"
# (3) D 3.044375 M' 96 with HP_MODE_EQUIL=1
t0=$(date +%s)
HP_MODE_EQUIL=1 nice -n 10 $PYN -u mequil_probe.py $WTN/hp probe_E_d3044_equil.jsonl $S96 5.140600 5.140819788786 5.1408197887863025 --threads=6 > probe_E_d3044_equil.log 2>&1 || stop 3 "probe E (D 3.044375, HP_MODE_EQUIL=1) failed"
python3 mequil_compare.py resolved probe_E_d3044_equil.jsonl --pair=5.140819788786,5.1408197887863025 --abs=1e-6 > mequil_resolved_E.txt 2>&1; rc=$?; rc3=$rc
step "(3) D 3.044375 M' 96, HP_MODE_EQUIL=1: pair exit $rc (0 = resolved), $(( $(date +%s) - t0 )) s; $(cut -c1-200 probe_E_d3044_equil.log | tr '\n' '|')"
echo "MEQUIL STEP 3 rc $rc $(stamp) UTC" > MEQUIL_STEP3_DONE.txt
if [ $rc3 = 0 ]; then
step "(4) starts: HP_MODE_EQUIL=1 lowD_gamma.py scan_mequil.jsonl <M' 96 state> --threads=6 --scan=5.14060,5.14100,21 (plan a: hmax 0.05, state unpolished)"
t0=$(date +%s)
( cd $WTN/hp && HP_MODE_EQUIL=1 nice -n 10 timeout 172800 $PYN -u lowD_gamma.py $OUT/scan_mequil.jsonl $S96 --threads=6 --scan=5.14060,5.14100,21 > $OUT/scan_mequil.log 2>&1 ); rc=$?
rc4=$rc
step "(4) scan: exit $rc, $(( $(date +%s) - t0 )) s, $(grep -c '"scan": true' scan_mequil.jsonl 2>/dev/null) points"
else
  step "(3) not resolved: no scan (4)"
  rc4=skipped
fi
# (1c) the selftest, lines equal to #1072's
t0=$(date +%s)
( cd $WTN/hp && env -u HP_MODE_EQUIL nice -n 10 $PYN lowD_gamma.py --selftest $S128U $S128M --threads=6 > $OUT/selftest_gp_D3.0444_M128_mequil_unset.txt 2>&1 ); g=$?
if diff -q $OLD selftest_gp_D3.0444_M128_mequil_unset.txt > /dev/null; then same=EQUAL; else same=DIFFERENT; fi
diff $OLD selftest_gp_D3.0444_M128_mequil_unset.txt > selftest_diff_mequil_vs_1072.txt 2>&1
step "(1c) lowD_gamma.py --selftest on the new kernel, unset: exit $g (0 wanted), lines against #1072's: $same, $(( $(date +%s) - t0 )) s"
echo "MEQUIL STEP 1 rc $g $same $(stamp) UTC" > MEQUIL_STEP1_DONE.txt
[ $g = 0 ] && [ $same = EQUAL ] || stop 1c "the selftest exit $g, lines $same"
echo "MEQUIL CHECKS DONE: step 3 rc $rc3, scan $rc4, selftest $g $same $(stamp) UTC" > MEQUIL_DONE.txt
exit 0
}
