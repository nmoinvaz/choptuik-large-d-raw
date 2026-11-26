#!/bin/bash
# #1025 kc119_d23_wide (t5's order, 26 Nov): macm3's k_c 119 state at D 23.0 (raw I1025-macm3/kc119_d23/in: state blob 2771cf87, record blob 158e3086) is accepted HERE, no regrid: kc119_syscheck_1025.py (fc6e0dd6) exit 0 on the
# state and record, its --mutate=F and --mutate=steps exit 1 each, and the k_c 111 check (85aeb312) refuses it (exit 1); both selftests exit 0. On ACCEPTED the state and record are copied to this folder and to the worktree's solver/matter/data/
# (blob checked), where run_scan.sh reads them. Writes steps.txt and VERDICT.txt (ACCEPTED or REFUSED). Memory: alert only. usage: run_accept.sh [dry]
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc119_d23_wide
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
step "start${MODE:+ (dry)}: accept macm3's k_c $TKC state at D $D (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB)"
while read -r h f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
RS=$IN/sol_${TAG}_${DT}.npy; RR=$IN/${TAG}.jsonl
[ "$(blob $RS | cut -c1-8)" = $STATE_BLOB ] && [ "$(blob $RR | cut -c1-8)" = $REC_BLOB ] || stop "the state or record is not $STATE_BLOB and $REC_BLOB"
[ "$(blob $IN/$ACC_CHK | cut -c1-8)" = $ACC_CHK_BLOB ] && [ "$(blob $IN/$OTHER_CHK | cut -c1-8)" = $OTHER_CHK_BLOB ] || stop "a check is not $ACC_CHK_BLOB / $OTHER_CHK_BLOB"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; state $STATE_BLOB, record $REC_BLOB, $ACC_CHK $ACC_CHK_BLOB, $OTHER_CHK $OTHER_CHK_BLOB)"
# the k_c 119 check is the k_c 111 check with a header comment line and three lines with 111 changed to 119 (macm3's reading; 3 lines removed, 4 added)
diff -u $IN/$OTHER_CHK $IN/$ACC_CHK > $OUT/kc119_check_vs_kc111.diff
nl=$(diff $IN/$OTHER_CHK $IN/$ACC_CHK | grep -c '^<'); nr=$(diff $IN/$OTHER_CHK $IN/$ACC_CHK | grep -c '^>')
[ "$nl" = 3 ] && [ "$nr" = 4 ] || stop "$ACC_CHK differs from $OTHER_CHK in $nl removed and $nr added lines (3 and 4 wanted)"
[ "$(diff $IN/$OTHER_CHK $IN/$ACC_CHK | grep '^<' | grep -c 111)" = 3 ] && [ "$(diff $IN/$OTHER_CHK $IN/$ACC_CHK | grep '^>' | grep -c 119)" = 4 ] || stop "the changed lines are not the k_c constants 111 -> 119 (and the header)"
step "$ACC_CHK = $OTHER_CHK with k_c 111 -> 119 in 3 lines and one header comment line (kc119_check_vs_kc111.diff)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
nice -n 10 $PY -I $IN/$ACC_CHK --selftest > $OUT/selftest_acc_check.txt 2>&1; r1=$?
nice -n 10 $PY -I $IN/$OTHER_CHK --selftest > $OUT/selftest_other_check.txt 2>&1; r2=$?
step "selftests: $ACC_CHK exit $r1, $OTHER_CHK exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
t0=$(date +%s)
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/$OTHER_CHK $RR $RS $D $WTM > $OUT/source_othercheck_refuses.txt 2>&1; s3=$?
kill $MEM 2>/dev/null
step "source check ($ACC_CHK on macm3's k_c $TKC D $D state, $(( $(date +%s) - t0 )) s for the four runs): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); $OTHER_CHK on it exit $s3 (1 wanted)"
if [ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ]; then
  cp $RS $OUT/; cp $RR $OUT/
  for f in sol_${TAG}_${DT}.npy ${TAG}.jsonl; do
    if [ -e $WTM/data/$f ]; then [ "$(blob $WTM/data/$f)" = "$(blob $IN/$f)" ] || stop "the worktree's $f differs from the pin"; else cp $IN/$f $WTM/data/$f; fi
    [ "$(blob $WTM/data/$f)" = "$(blob $IN/$f)" ] || stop "copied $f differs"
  done
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: $ACC_CHK $s0, controls $s1 $s2, $OTHER_CHK refuses $s3" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
