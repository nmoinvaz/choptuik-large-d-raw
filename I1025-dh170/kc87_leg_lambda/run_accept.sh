#!/bin/bash
# #1025 kc87_leg_lambda (t5's order, 24 Nov): no regrid. One state of dh370's k_c 87 leg (raw I1025-dh370/kc87_leg/, tag l1kc87Ldh370), pinned by blob in <D>/in/, is accepted HERE by dh610's kc87_syscheck_1025.py
# (6df5d960) with its two controls (both exit 1); the k_c 79 check (29dce7ea) must refuse it (exit 1); both selftests exit 0; kc87_syscheck is kc79_syscheck with 3 lines changed (checked). Writes <D>/steps.txt and <D>/VERDICT.txt
# (ACCEPTED or REFUSED) and copies the pinned state and record to <D>/ and to the worktree's solver/matter/data/ (blob checked); an older data/<tag>.jsonl of the same tag (an earlier D's record, pinned in that D's folder) is
# moved aside (renamed with its blob), never deleted. usage: run_accept.sh <D folder> [dry]
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc87_leg_lambda
STAGE=${1:?the D folder, e.g. 21.03125}; MODE=${2:-}
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
    if [ -e $WTM/data/$f ] && [ "$(blob $WTM/data/$f)" != "$(blob $IN/$f)" ]; then
      case $f in *.jsonl) ob=$(blob $WTM/data/$f | cut -c1-8); mv $WTM/data/$f $WTM/data/$f.${ob}_superseded; step "the worktree's $f (blob $ob) differs from the pin: moved aside to $f.${ob}_superseded, not deleted";;
      *) stop "the worktree's $f differs from the pin";; esac
    fi
    [ -e $WTM/data/$f ] || cp $IN/$f $WTM/data/$f
    [ "$(blob $WTM/data/$f)" = "$(blob $IN/$f)" ] || stop "copied $f differs"
  done
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: $ACC_CHK $a0, controls $a1 $a2, $SRC_CHK refuses $a3" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
