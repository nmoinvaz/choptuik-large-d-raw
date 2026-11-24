#!/bin/bash
# #1078, t5's order (comment of 00:35 UTC; unit i1078y: the rerun on main ba473990, whose mode_qd.py (blob d20a85fe) calls multidouble._md.qd_logdet with its control; unit i1078x stopped at the selftest on b2440b73), after the lambda 8 row and the D 3.15 Jacobian control (unit i1078w), 4 threads, nice 10, beside the #1080 control: hp/mode_qd.py (main ba473990,
# blob d20a85fe; worktree ~/Source/choptuik-large-d-1078q, python and kernel of ~/Source/choptuik-large-d-1078m: a2607acb build, multidouble's package with qd_logdet) on the D 3.044375 M' 96 state 6a0f83d2, hmax 0.05:
# (1) mode_qd.py selftest (PASS and its --control=update_dd control fires); (2) the pair lambda 5.140819788786 and 5.1408197887863025 (resolved = the same sign and ln|det| within 1e-6, mequil_compare.py resolved),
# then the same pair with --control=update_dd (trailing updates in double-double: must jag, about 3 in ln|det|); (3) seconds per lambda. Log: steps_modeqd.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WTQ=/home/nathan/Source/choptuik-large-d-1078q
WTM=/home/nathan/Source/choptuik-large-d-1078m
PY=$WTM/.venv/bin/python
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
L1=5.140819788786; L2=5.1408197887863025
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4
unset HP_DENSE_M_MAX HP_MODE_EQUIL
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_modeqd.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_MODEQD_$1.txt; step "STOP $1: $2"; echo "MODEQD STOPPED at $1 $(stamp) UTC" > $OUT/MODEQD_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $WTQ/hp || exit 9
[ "$(git -C $WTQ rev-parse --short=8 HEAD)" = ba473990 ] && [ "$(blob mode_qd.py)" = d20a85fe ] && [ "$(git -C $WTM rev-parse --short=8 HEAD)" = a2607acb ] && [ "$(blob $S96)" = 6a0f83d2 ] || stop 0 "a worktree, mode_qd.py or the state not pinned"
step "start; multidouble $($PY -c 'import multidouble as m; print(m.isa(), hasattr(m, "qd_logdet"))' 2>/dev/null); load $(cut -d' ' -f1-3 /proc/loadavg)"
# (1)
$PY mode_qd.py selftest > $OUT/modeqd_selftest.txt 2>&1; rc=$?
step "(1) mode_qd.py selftest: exit $rc (0 wanted); $(grep -v Warning $OUT/modeqd_selftest.txt | cut -c1-400)"
[ $rc = 0 ] || stop 1 "the selftest did not pass"
# (2) the pair
t0=$(date +%s)
nice -n 10 $PY -u mode_qd.py $OUT/modeqd_pair.jsonl $S96 $L1 $L2 --threads=4 > $OUT/modeqd_pair.log 2>&1; rc=$?
step "(2) qd pair: exit $rc, $(( $(date +%s) - t0 )) s; $(grep -v Warning $OUT/modeqd_pair.log | cut -c1-250 | tr '\n' '|')"
[ $rc = 0 ] || stop 2 "mode_qd pair exit $rc"
python3 $OUT/mequil_compare.py resolved $OUT/modeqd_pair.jsonl --pair=$L1,$L2 --abs=1e-6 > $OUT/modeqd_pair_resolved.txt 2>&1; rcr=$?
step "(2) the pair, resolved = same sign and ln|det| within 1e-6: exit $rcr (0 = resolved); $(head -1 $OUT/modeqd_pair_resolved.txt | cut -c1-300)"
echo "MODEQD STEP 2 rc $rcr $(stamp) UTC" > $OUT/MODEQD_STEP2_DONE.txt
# (2c) the control: the same pair with the trailing updates in double-double
t0=$(date +%s)
nice -n 10 $PY -u mode_qd.py $OUT/modeqd_pair_control.jsonl $S96 $L1 $L2 --threads=4 --control=update_dd > $OUT/modeqd_pair_control.log 2>&1; rc=$?
step "(2c) control update_dd pair: exit $rc, $(( $(date +%s) - t0 )) s; $(grep -v Warning $OUT/modeqd_pair_control.log | cut -c1-250 | tr '\n' '|')"
python3 $OUT/mequil_compare.py resolved $OUT/modeqd_pair_control.jsonl --pair=$L1,$L2 --abs=1e-6 > $OUT/modeqd_pair_control_resolved.txt 2>&1; rcc=$?
step "(2c) the control pair against the same bar: exit $rcc (1 wanted: it must jag); $(head -1 $OUT/modeqd_pair_control_resolved.txt | cut -c1-300)"
echo "MODEQD DONE: pair resolved exit $rcr, control pair exit $rcc $(stamp) UTC" > $OUT/MODEQD_DONE.txt
exit 0
}
