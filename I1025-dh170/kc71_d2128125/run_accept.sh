#!/bin/bash
# #1025 kc71_d2128125 (t5's order, 24 Nov): no regrid. win2's k_c 71 leg 6 state at D 21.28125 (raw I1025-win2/kc71_leap/, commit 2f39b042, tag l1kc71Lw1025e), pinned by blob in in/, is accepted HERE by kc71_syscheck.py
# (4cd86cd4) with its two controls (both exit 1); as an extra control the k_c 79 check must refuse it (exit 1); both selftests exit 0. Writes steps.txt and VERDICT.txt (ACCEPTED or REFUSED) and copies the pinned state and
# record to this folder and to the worktree's solver/matter/data/ (blob checked), where run_scan.sh reads them. NODIFF=1 in stage.conf skips the 3-line diff check. usage: run_accept.sh [dry]
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc71_d2128125
MODE=${1:-}
OUT=$ROOT; IN=$OUT/in
WT=/home/nathan/Source/choptuik-large-d-1025k79
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
[ -f $OUT/stage.conf ] || { echo "no $OUT/stage.conf"; exit 9; }
. $OUT/stage.conf
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
[ -e $OUT/VERDICT.txt ] && [ "$MODE" != dry ] && { echo "VERDICT.txt exists"; exit 2; }
step "start${MODE:+ ($MODE)} accept another machine's k_c $TKC state at D $D (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB)"
while read -r h f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
RS=$IN/sol_${TAG}_${DT}.npy; RR=$IN/${TAG}.jsonl
[ -s $RS ] && [ -s $RR ] || stop "the pinned state or record is missing or empty"
[ "$(blob $RS | cut -c1-8)" = $RES_STATE_BLOB ] && [ "$(blob $RR | cut -c1-8)" = $RES_REC_BLOB ] || stop "the state or record is not $RES_STATE_BLOB and $RES_REC_BLOB"
[ "$(blob $IN/$SRC_CHK | cut -c1-8)" = $SRC_CHK_BLOB ] && [ "$(blob $IN/$ACC_CHK | cut -c1-8)" = $ACC_CHK_BLOB ] || stop "a check is not $SRC_CHK_BLOB / $ACC_CHK_BLOB"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; state $RES_STATE_BLOB, record $RES_REC_BLOB, $SRC_CHK $SRC_CHK_BLOB, $ACC_CHK $ACC_CHK_BLOB)"
if [ -z "${NODIFF:-}" ]; then
  diff -u $IN/$SRC_CHK $IN/$ACC_CHK > $OUT/check_diff_rebuilt.txt
  nl=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^<'); nr=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^>')
  [ "$nl" = 3 ] && [ "$nr" = 3 ] || stop "$ACC_CHK differs from $SRC_CHK in $nl and $nr lines (3 and 3 wanted)"
  step "$ACC_CHK = $SRC_CHK with 3 lines changed (check_diff_rebuilt.txt)"
else
  step "$ACC_CHK and $SRC_CHK are unrelated checks here (NODIFF): the source check is $ACC_CHK $ACC_CHK_BLOB, refused by $SRC_CHK $SRC_CHK_BLOB"
fi
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
nice -n 10 $PY -I $IN/$ACC_CHK --selftest > $OUT/selftest_acc_check.txt 2>&1; r1=$?
nice -n 10 $PY -I $IN/$SRC_CHK --selftest > $OUT/selftest_src_check.txt 2>&1; r2=$?
step "selftests: $ACC_CHK exit $r1, $SRC_CHK exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $IN/$SRC_CHK $RR $RS $D $WTM > $OUT/syscheck_srccheck_refuses.txt 2>&1; a3=$?
step "$ACC_CHK exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); $SRC_CHK on the k_c $TKC state exit $a3 (1 wanted)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then
  # the scan reads the state and record from the stage folder and the worktree's data/ (blob checked)
  cp $RS $OUT/; cp $RR $OUT/
  for f in sol_${TAG}_${DT}.npy ${TAG}.jsonl; do
    if [ -e $WTM/data/$f ]; then [ "$(blob $WTM/data/$f)" = "$(blob $IN/$f)" ] || stop "the worktree's $f differs from the pin"; else cp $IN/$f $WTM/data/$f; fi
    [ "$(blob $WTM/data/$f)" = "$(blob $IN/$f)" ] || stop "copied $f differs"
  done
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: $ACC_CHK $a0, controls $a1 $a2, $SRC_CHK refuses $a3" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
