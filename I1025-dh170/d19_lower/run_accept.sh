#!/bin/bash
# #1025 d19_lower stage k95 (t5's hc, 23 Nov, after the stage k87 regrid had started): no regrid on this machine. The k_c 95 state and record are another machine's regrid (dh610's, tag l1kc95dh610d19, raw
# I1025-dh610/d19_k95/, made from my accepted k_c 87 state), pinned by blob in <stage>/in/ and accepted HERE by dh610's kc95_syscheck_1025.py with its two controls (both exit 1), the k_c 87 check refusing it
# (exit 1), both selftests exit 0. Writes <stage>/steps.txt and <stage>/VERDICT.txt (ACCEPTED or REFUSED) and copies the pinned state and record to <stage>/ and to the worktree's solver/matter/data/ (blob checked),
# where run_scan.sh reads them. 8 threads are not needed (the checks are short). Memory: nothing here is long. usage: run_accept.sh <stage> [dry]
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/d19_lower
STAGE=${1:?stage k95}; MODE=${2:-}
OUT=$ROOT/$STAGE; IN=$OUT/in
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
step "start${MODE:+ ($MODE)} stage $STAGE: accept another machine's k_c $TKC state at D $D (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB)"
while read -r h f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
RS=$IN/sol_${TAG}_${DT}.npy; RR=$IN/${TAG}.jsonl
[ -s $RS ] && [ -s $RR ] || stop "the pinned state or record is missing or empty"
[ "$(blob $RS | cut -c1-8)" = $RES_STATE_BLOB ] && [ "$(blob $RR | cut -c1-8)" = $RES_REC_BLOB ] || stop "the state or record is not $RES_STATE_BLOB and $RES_REC_BLOB"
[ "$(blob $IN/$SRC_CHK | cut -c1-8)" = $SRC_CHK_BLOB ] && [ "$(blob $IN/$ACC_CHK | cut -c1-8)" = $ACC_CHK_BLOB ] || stop "a check is not $SRC_CHK_BLOB / $ACC_CHK_BLOB"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; state $RES_STATE_BLOB, record $RES_REC_BLOB, $SRC_CHK $SRC_CHK_BLOB, $ACC_CHK $ACC_CHK_BLOB)"
diff -u $IN/$SRC_CHK $IN/$ACC_CHK > $OUT/check_diff_rebuilt.txt
nl=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^<'); nr=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^>')
[ "$nl" = 3 ] && [ "$nr" = 3 ] || stop "$ACC_CHK differs from $SRC_CHK in $nl and $nr lines (3 and 3 wanted)"
step "$ACC_CHK = $SRC_CHK with 3 lines changed (check_diff_rebuilt.txt)"
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
