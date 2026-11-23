#!/bin/bash
# #1025 kc79_d2025 on win2, STEP 3 (the coordinator's task, comment 7093559078; hc ~08:00 UTC 23 Nov): k_c 87 at D 20.25 from win2's own accepted k_c 79 D 20.25 state (step 1, this folder), as at D 20 (../kc87_d20/):
#   ell_refine.py l1kc79win2d2025 79 l1kc87win2d2025 87 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
# Source: kc79_syscheck_1025.py (29dce7ea) accepts it (--mutate=F and --mutate=steps exit 1) and kc87_syscheck_1025.py (6df5d960) refuses it. Result accepted only by kc87_syscheck_1025.py (selftest 0, --mutate=F and
# --mutate=steps exit 1) with kc79_syscheck_1025.py refusing it. 8 threads, Normal priority (the launcher), cap 21600 s by the exact pid; no retry.
# WHEN: the coordinator allowed it beside step 2's scan (hc ~08:00 UTC): this driver waits for the k_c 79 regrid's acceptance (regrid_accepted.txt non-empty), gives the scan 2 minutes to ramp up, and starts only if at least 8
# logical cores are idle then (CPU load, mean of 5 samples; the other project's jobs count as busy); otherwise it waits for step 2's end (scan.done, or a refused regrid) and starts then. usage: regrid87_d2025.sh   (DRY=1: the gate, the source checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_d2025   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc87.txt; SUM=$OUT/summary_kc87.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data; WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_d2025
SRC=l1kc79win2d2025; TAG=l1kc87win2d2025; STD=20.25; F4=20.2500; LAM0=2.1099063840
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
refuse() { log "kc87 d2025 regrid STOP: $*"; echo "kc87 d2025 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid87_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc87 d2025 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/inputs/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc87 d2025 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc87 d2025 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $DATA/sol_${TAG}_D${F4}.npy $OUT/regrid87_accepted.txt $OUT/regrid87_refused.txt; do [ -e $f ] && { log "kc87 d2025 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc87 d2025 regrid pins checked (kc79 check 29dce7ea, kc87 check 6df5d960, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399); waits for the k_c 79 regrid's acceptance"
until [ -s $OUT/regrid_accepted.txt ]; do [ -e $OUT/regrid_refused.txt ] && { log "kc87 d2025 regrid: the k_c 79 regrid was refused: nothing to regrid"; exit 3; }; sleep 30; done
log "kc87 d2025 regrid: the k_c 79 regrid is accepted; the scan ramps up (120 s), then the cores are checked"
sleep 120
idle_cores() { powershell -NoProfile -Command "\$s = (Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 2 -MaxSamples 5).CounterSamples | ForEach-Object { \$_.CookedValue }; \$m = (\$s | Measure-Object -Average).Average; [math]::Round(20 * (1 - \$m / 100), 1)" | tr -d '\r'; }
IDLE=$(idle_cores)
if [ "$(python -I -c "print(1 if float('${IDLE:-0}') >= 8 else 0)")" = 1 ]; then
  log "kc87 d2025 regrid: $IDLE logical cores idle (at least 8 needed): starting beside step 2's scan"
else
  log "kc87 d2025 regrid: only $IDLE logical cores idle (8 needed): waiting for step 2 to end (scan.done)"
  until [ -e $OUT/scan.done ]; do sleep 30; done
  log "kc87 d2025 regrid: step 2 ended: starting"
fi
cd $OUT
RECS=$OUT/${SRC}.jsonl; STS=$OUT/sol_${SRC}_D${F4}.npy
chk $DATA/sol_${SRC}_D${F4}.npy "" "the worktree's k_c 79 D 20.25 state"
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy)" = "$(git hash-object --no-filters $STS)" ] || refuse "the worktree's k_c 79 state differs from the accepted copy"
log "kc87 d2025 regrid source: state $(git hash-object --no-filters $STS | cut -c1-8), record file $(git hash-object --no-filters $RECS | cut -c1-8)"
"$PY" -I inputs/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1; [ $? = 0 ] || refuse "kc87_syscheck_1025.py --selftest did not exit 0"
"$PY" -I inputs/kc79_syscheck_1025.py $RECS $STS $STD $WTM > source_kc79_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc79_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc79_syscheck_1025.py does not accept the k_c 79 source (exit $s)"
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $RECS $STS $STD $WTM --mutate=$m > source_kc79_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m (k_c 79 check) did not exit 1"; done
"$PY" -I inputs/kc87_syscheck_1025.py $RECS $STS $STD $WTM > source_kc87_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED)' source_kc87_syscheck.txt >> $SUM
[ $s = 1 ] || refuse "kc87_syscheck_1025.py did not refuse the k_c 79 source (exit $s)"
log "kc87 d2025 regrid: the k_c 79 D 20.25 source is accepted by the k_c 79 check (controls exit 1) and refused by the k_c 87 check"
CMD="$PY -u ell_refine.py $SRC 79 $TAG 87 1 $STD $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, cap 21600 s)"; log "kc87 d2025 regrid DRY run ended before the regrid"; exit 0; }
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/regrid87.log
s0=$(date +%s)
crun regrid87b 0 21600 ell_refine.py $CMD >> $OUT/regrid87.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid87.log
echo "kc87 d2025 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc87 d2025 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${TAG}_D${F4}.npy ] && [ -s $DATA/${TAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${TAG}_D${F4}.npy $DATA/${TAG}.jsonl $OUT/
cd $OUT
"$PY" -I inputs/kc87_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM > syscheck87.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck87.txt >> $SUM
[ $s = 0 ] || refuse "kc87_syscheck_1025.py does not accept the k_c 87 state (exit $s)"
for m in F steps; do "$PY" -I inputs/kc87_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM --mutate=$m > syscheck87_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM > syscheck_kc79_on_k87_result.txt 2>&1; [ $? = 1 ] || refuse "kc79_syscheck_1025.py did not refuse the k_c 87 result"
tail -n 1 $OUT/${TAG}.jsonl > $OUT/rec_k87_D${F4}.jsonl
"$PY" -I -c "
import json
a = json.loads(open('$WOUT/rec_k79_D${F4}.jsonl').read().strip().splitlines()[-1]); b = json.loads(open('$WOUT/rec_k87_D${F4}.jsonl').read().strip().splitlines()[-1])
print('ACCEPTED: k_c 79 source |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 87 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 87 minus k_c 79 %.4e), regrid %s s' % (a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
" > $OUT/regrid87_accepted.txt
[ -s $OUT/regrid87_accepted.txt ] || refuse "regrid87_accepted.txt is empty (the summary step failed)"
cat $OUT/regrid87_accepted.txt >> $SUM; log "kc87 d2025 regrid ACCEPTED: $(cut -c1-220 $OUT/regrid87_accepted.txt)"
touch $OUT/regrid87.done
exit 0
