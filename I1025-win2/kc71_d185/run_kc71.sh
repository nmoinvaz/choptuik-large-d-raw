#!/bin/bash
# #1025 kc71_d185 on win2 (the coordinator's hc of 2026-11-21 ~23:05 UTC): a third k_c at D 18.5. Part 1: regrid the k_c 63 D 18.5 state (I1025-mac/d18/sol_l1kc63Wm1025_D18.5000.npy, blob 33c1a58b, = ..._D18.500000.npy) to k_c 71
# with ell_refine.py --no-gamma (no lambda search): `ell_refine.py l1kc63Wm1025 63 l1kc71Wm1025 71 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma` in a clean worktree
# (D:/choptuik-i1025k71 at 48c36355), 4 threads, BelowNormal (the caller sets it), cap 21600 s by the exact root pid. The state is accepted only by kc71_syscheck.py (the record class's |F| <= 1e-9 and the step count and |F| coming back on the saved
# state, with two controls); if the regrid does not converge (exit, cap, no state or record, not accepted) the task stops with a report and no scan starts. Part 2: xfkappa's d18_hybsign.py on the accepted state, lambda 1.55 to 2.49 at 0.02
# (48 points), four processes, 4 threads each, caps 28800 s by the exact root pids: P1 = 1.77 then 1.55 to 1.75 (12 evaluations); P2 = 1.77 then 1.79 to 2.01 (13); P3 = 2.25 then 2.03 to 2.23 (12); P4 = 2.25 then 2.27 to 2.49 (13); the pairs
# (P1, P2) and (P3, P4) each repeat one point (1.77, 2.25) evaluated first in both; the pair gate (pair_check.py) compares them when the first points exist and kills all four scans by exact pid on a disagreement. Then kc71_read.py.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_d185
. $OUT/lib_kc71.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_d185
RAWR=D:/choptuik-large-d-raw-push
Q=$RAWR/I1025-mac/d18
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
TAG=l1kc71Wm1025
CAPRG=21600
CAP=28800
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
bad=0
chk() { # path blob-prefix label
  local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "refuse: $3 is blob $h, not $2"; bad=1;; esac
}
chk $Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2 "d18_hybsign.py"
chk $Q/sol_l1kc63Wm1025_D18.5000.npy 33c1a58b "the k_c 63 D 18.5 state (raw)"
chk $OUT/inputs/sol_l1kc63Wm1025_D18.5000.npy 33c1a58b "the k_c 63 D 18.5 state (inputs copy)"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
for pr in "d18d_read.py 6b608903" "d185_scan_read.py 7c9d400f" "d18c_read.py 1383470f"; do set -- $pr; chk /d/choptuik-i935-raw/I1025-win2/d18mid/pinned/$1 $2 "pinned/$1"; done
for pr in "d185_scan_1025.jsonl 90540daf" "d185_scanhi_1025.jsonl 496f4b63" "d185_scanup_1025.jsonl 9f3e31e5" "kc55_scan_merged.jsonl 24179d07" "kc63_map_A_new.jsonl 071f03fd" "kc63_map_B_new.jsonl aebb87db"; do set -- $pr; chk $OUT/inputs/$1 $2 "inputs/$1"; done
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py || { log "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in $WT/solver/matter/data/sol_${TAG}_D18.5000.npy $WT/solver/matter/data/${TAG}.jsonl $OUT/scan_P1.jsonl $OUT/scan_P2.jsonl $OUT/scan_P3.jsonl $OUT/scan_P4.jsonl; do [ -e $f ] && { log "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "pins checked: d18_hybsign e089207a, the k_c 63 state 33c1a58b, ell_refine.py 631e5801, the pinned readers, the inputs (blobs in inputs/BLOBS.txt), worktree 48c36355 with solver code = 505d8399 and ell_delta = 48c36355, venv-md510"
cd $OUT
"$PY" kc71_syscheck.py --selftest > selftest_syscheck.txt 2>&1; s1=$?
"$PY" kc71_read.py --selftest > selftest_read71.txt 2>&1; s2=$?
"$PY" kc71_read.py --selftest --break > selftest_read71_break.txt 2>&1; s3=$?
"$PY" pair_check.py --selftest > selftest_pair.txt 2>&1; s4=$?
"$PY" pair_check.py --selftest --break > selftest_pair_break.txt 2>&1; s5=$?
"$PY" D:/choptuik-i935-raw/I1025-win2/d18mid/pinned/d18d_read.py selftest > selftest_read.txt 2>&1; s6=$?
"$PY" D:/choptuik-i935-raw/I1025-win2/d18mid/pinned/d18d_read.py selftest --mutate=orient > selftest_read_mutate.txt 2>&1; s7=$?
echo "controls: kc71_syscheck selftest $s1 (0); kc71_read selftest $s2 (0), --break $s3 (1); pair_check selftest $s4 (0), --break $s5 (1); d18d_read selftest $s6 (0), --mutate=orient $s7 (1)" >> $SUM; log "controls $s1 $s2/$s3 $s4/$s5 $s6/$s7"
[ $s1 = 0 ] && [ $s2 = 0 ] && [ $s3 = 1 ] && [ $s4 = 0 ] && [ $s5 = 1 ] && [ $s6 = 0 ] && [ $s7 = 1 ] || { log "a control is wrong: stop"; exit 1; }
# ---- part 1: the regrid
cp $OUT/inputs/sol_l1kc63Wm1025_D18.5000.npy $WT/solver/matter/data/sol_l1kc63Wm1025_D18.5000.npy
chk $WT/solver/matter/data/sol_l1kc63Wm1025_D18.5000.npy 33c1a58b "the state copied into the worktree"
[ $bad = 0 ] || exit 2
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $PY -u ell_refine.py l1kc63Wm1025 63 $TAG 71 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (cwd $WTM, 4 threads)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid 0 $CAPRG ell_refine.py "$PY" -u ell_refine.py l1kc63Wm1025 63 $TAG 71 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAPRG s")" >> $SUM; log "regrid exit $rc wall $w s capped $CAPPED"
stop() { echo "$1" >> $SUM; log "$1"; echo "kc71 stopped: the regrid did not converge" >> $SUM; touch $OUT/all.done; exit 0; }
[ $rc = 0 ] || stop "the regrid did not finish (exit $rc): the task stops with a report; no scan starts"
[ -s data/sol_${TAG}_D18.5000.npy ] && [ -s data/${TAG}.jsonl ] || stop "the regrid wrote no state or record: the task stops with a report; no scan starts"
cp data/sol_${TAG}_D18.5000.npy data/${TAG}.jsonl $OUT/
cd $OUT
s0=$(date +%s)
"$PY" kc71_syscheck.py $WOUT/${TAG}.jsonl $WOUT/sol_${TAG}_D18.5000.npy 18.5 $WTM > syscheck.txt 2>&1; ac=$?
echo "acceptance check: exit $ac, $(( $(date +%s) - s0 )) s: $(grep -E '^(ACCEPTED|NOT ACCEPTED)' syscheck.txt)" >> $SUM; log "acceptance exit $ac"
[ $ac = 0 ] || stop "the regridded state is not accepted ($(grep -E '^NOT ACCEPTED' syscheck.txt | cut -c1-200)): the task stops with a report; no scan starts"
# ---- part 2: the scan
LP1=$("$PY" -c 'g=[round(1.55 + 0.02 * i, 2) for i in range(48)]; print(",".join("%.2f" % x for x in [1.77] + [x for x in g[0:12] if x != 1.77]))')
LP2=$("$PY" -c 'g=[round(1.55 + 0.02 * i, 2) for i in range(48)]; print(",".join("%.2f" % x for x in [1.77] + g[12:24]))')
LP3=$("$PY" -c 'g=[round(1.55 + 0.02 * i, 2) for i in range(48)]; print(",".join("%.2f" % x for x in [2.25] + [x for x in g[24:36] if x != 2.25]))')
LP4=$("$PY" -c 'g=[round(1.55 + 0.02 * i, 2) for i in range(48)]; print(",".join("%.2f" % x for x in [2.25] + g[36:48]))')
log "lambda list P1: $LP1"; log "lambda list P2: $LP2"; log "lambda list P3: $LP3"; log "lambda list P4: $LP4"
cd $WT/solver/matter || exit 1
scan() {  # P LAMS
  local P=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $WOUT/${TAG}.jsonl $WOUT/sol_${TAG}_D18.5000.npy 18.5 $L $WOUT/scan_$P.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_$P.log
  crun scan_$P 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $WOUT/${TAG}.jsonl $WOUT/sol_${TAG}_D18.5000.npy 18.5 $L $WOUT/scan_$P.jsonl >> $OUT/scan_$P.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_$P.log
  local n; n=$(grep -c '^{' $OUT/scan_$P.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_$P: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scan_$P exit $rc wall $w s capped $CAPPED"
}
killroot() {  # NAME: the exact root pid of crun NAME, after its command line is checked
  local pid; pid=$(grep " $1 root pid " $EX | tail -1 | sed -E 's/.* root pid ([0-9]+),.*/\1/')
  [ -n "$pid" ] || return
  local cl; cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
  case "$cl" in *d18_hybsign.py*) log "gate: killing the tree of $1 pid $pid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;; *) log "gate: $1 pid $pid does not match d18_hybsign.py (${cl:0:60}), nothing killed";; esac
}
scan P1 $LP1 &
q1=$!
scan P2 $LP2 &
q2=$!
scan P3 $LP3 &
q3=$!
scan P4 $LP4 &
q4=$!
t0=$(date +%s); gate=none
while kill -0 $q1 2> /dev/null || kill -0 $q2 2> /dev/null || kill -0 $q3 2> /dev/null || kill -0 $q4 2> /dev/null; do
  "$PY" $OUT/pair_check.py $WOUT > $OUT/pair_check.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "pair gate passed"; echo "pair gate: passed after $(( $(date +%s) - t0 )) s: $(grep '^PAIRS' $OUT/pair_check.txt)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "pair gate FAILED: a repeated point disagrees; killing all four scans"; echo "pair gate: FAILED: $(grep -E 'DISAGREE' $OUT/pair_check.txt | head -n 2 | tr '\n' ' ')" >> $SUM; for n in P1 P2 P3 P4; do killroot scan_$n; done; break; fi
  if [ $(( $(date +%s) - t0 )) -gt 7200 ]; then gate=fail; log "pair gate: no first points after 7200 s; killing all four scans"; echo "pair gate: no first points after 7200 s" >> $SUM; for n in P1 P2 P3 P4; do killroot scan_$n; done; break; fi
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "pair gate: the scans ended before the first points were compared" >> $SUM; }
wait $q1; wait $q2; wait $q3; wait $q4
cd $OUT
if [ $gate = pass ]; then
  "$PY" kc71_read.py $WOUT > kc71_read.txt 2>&1
  echo "kc71_read: exit $?: $(grep -E '^(OVERALL|STOP-level|CONTROL FAILED)' kc71_read.txt | cut -c1-250)" >> $SUM
fi
"$PY" points_table_kc71.py $WOUT > points_kc71.md 2>&1
echo "points_table_kc71: exit $?" >> $SUM
log "done (gate $gate)"; echo "kc71 done (pair gate $gate)" >> $SUM
touch $OUT/all.done
exit 0
