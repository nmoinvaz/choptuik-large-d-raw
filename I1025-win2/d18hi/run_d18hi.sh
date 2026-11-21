#!/bin/bash
# #1025 d18hi on win2 (the coordinator's hc of 2026-11-21 ~16:15 UTC, after d18mid). Part 1, the control: the Mac's D 18 point at lambda 1.8 (lane_d18b.sh's call: d18_hybsign.py STUB STATE 18 1.8 OUT, state 45e72c6a, stub 2cfdb833)
# on win2, 4 threads, BelowNormal (the caller sets it), cap 3600 s by the exact root pid; ctl_check.py reads it (the Mac: +1, ln -1925.018228986828). If the control fails (a different sign, ln off by more than 1e-2, a
# non-robust point, or no finish) the scan is NOT started and the run stops there (AGENTS.md: a control that fires on real data stops the work). Part 2: xfkappa's hybrid sign scan at D 18.1875 above the d18mid window, lambda 1.95
# to 2.35 at 0.01 (41 points), TWO processes side by side with 1.95 in both as the check (A: 1.95 to 2.15, 21 points; B: 1.95, then 2.16 to 2.35, 21 points), 4 threads each, each capped at 28800 s by the exact root pid, venv-md510.
# Then xfkappa's reader (d18d_read.py, blob 6b608903) on the two files (this window) and on all four (d18mid's two and these two, 1.70 to 2.35), and points_table.py.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/d18hi
. $OUT/lib_d18hi.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/d18hi
WMID=D:/choptuik-i935-raw/I1025-win2/d18mid
RAWR=D:/choptuik-large-d-raw-push
Q=$RAWR/I1025-mac/d18
WT=/d/choptuik-i1025d
WTM=D:/choptuik-i1025d/solver/matter
REC=$Q/l1kc63Wm1025.jsonl
ST18=$Q/sol_l1kc63W1025_D18.000000.npy
STUB=$Q/d18_stub_l1kc63W1025.jsonl
STHI=$Q/sol_l1kc63Wm1025_D18.187500.npy
CAP=28800
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
declare -A BLOB=( [d18_hybsign.py]=e089207a61fbd98614716abd309571cbc4888db2 [d18d_read.py]=6b608903 [d185_scan_read.py]=7c9d400fd0966a35ac306b5495febb4ec4efe7da [d18c_read.py]=1383470feaa976e4185e423626a0d5fec328de86
                  [sol_l1kc63W1025_D18.000000.npy]=45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21 [d18_stub_l1kc63W1025.jsonl]=2cfdb8334ed6ba7013396190d8a4833b2b854c4b
                  [sol_l1kc63Wm1025_D18.187500.npy]=3f06b92e [l1kc63Wm1025.jsonl]=08f4dbf3 )
bad=0
for f in "${!BLOB[@]}"; do
  h=$(git hash-object --no-filters /d/choptuik-large-d-raw-push/I1025-mac/d18/$f)
  case "$h" in ${BLOB[$f]}*) ;; *) log "refuse: $f is blob $h, not ${BLOB[$f]}"; bad=1;; esac
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py || { log "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in ctl_D18_lam1.8.jsonl scan_hi_D18.1875_A.jsonl scan_hi_D18.1875_B.jsonl; do [ -e $OUT/$f ] && { log "refuse: $f exists (d18_hybsign appends)"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "pins checked: d18_hybsign e089207a, d18d_read 6b608903, d185_scan_read 7c9d400f, d18c_read 1383470f, D 18 state 45e72c6a, stub 2cfdb833, D 18.1875 state 3f06b92e, record 08f4dbf3, solver code = 505d8399 (dss_ell, ell_ddm, ell_dd, ddnp), ell_delta = 48c36355 (worktree $(git -C $WT rev-parse --short HEAD)), venv-md510"
cd $OUT
"$PY" ctl_check.py --selftest > selftest_ctl.txt 2>&1; c1=$?
"$PY" ctl_check.py --selftest --break > selftest_ctl_break.txt 2>&1; c2=$?
"$PY" $Q/d18d_read.py selftest > selftest_read.txt 2>&1; r1=$?
"$PY" $Q/d18d_read.py selftest --mutate=orient > selftest_read_mutate.txt 2>&1; r2=$?
echo "controls: ctl_check selftest exit $c1 (0), --break exit $c2 (1); d18d_read selftest exit $r1 (0), --mutate=orient exit $r2 (1)" >> $SUM; log "controls ctl_check $c1/$c2 reader $r1/$r2"
[ $c1 = 0 ] && [ $c2 = 1 ] && [ $r1 = 0 ] && [ $r2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
# ---- part 1: the cross-machine control
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $STUB $ST18 18 1.8 $WOUT/ctl_D18_lam1.8.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/ctl_D18_lam1.8.log
s0=$(date +%s)
crun ctl_D18_lam1.8 0 3600 d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $STUB $ST18 18 1.8 $WOUT/ctl_D18_lam1.8.jsonl >> $OUT/ctl_D18_lam1.8.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/ctl_D18_lam1.8.log
"$PY" $OUT/ctl_check.py $WOUT/ctl_D18_lam1.8.jsonl > ctl_check.txt 2>&1; cc=$?
echo "control D 18 lambda 1.8: exit $rc, $w s, ctl_check exit $cc: $(grep '^CONTROL' ctl_check.txt)" >> $SUM
log "control exit $rc wall $w s ctl_check $cc"
if [ $rc != 0 ] || [ $cc != 0 ]; then
  echo "the control did not pass (run exit $rc, ctl_check exit $cc): the scan is NOT started; the run stops and reports" >> $SUM
  log "control failed: the scan is not started"; echo "d18hi stopped at the control" >> $SUM; touch $OUT/all.done; exit 0
fi
# ---- part 2: the scan above the window
LA=$("$PY" -c 'print(",".join(f"{1.95 + 0.01 * i:.2f}" for i in range(21)))')
LB=$("$PY" -c 'print("1.95," + ",".join(f"{2.16 + 0.01 * i:.2f}" for i in range(20)))')
log "lambda list A (21): $LA"
log "lambda list B (check point 1.95, then 20): $LB"
D=18.1875
scan() {  # P LAMS
  local P=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $REC $STHI $D $L $WOUT/scan_hi_D${D}_$P.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_hi_D${D}_$P.log
  crun scan_$P 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $REC $STHI $D $L $WOUT/scan_hi_D${D}_$P.jsonl >> $OUT/scan_hi_D${D}_$P.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_hi_D${D}_$P.log
  local n; n=$(grep -c '^{' $OUT/scan_hi_D${D}_$P.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_hi_D${D}_$P: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scan_$P exit $rc wall $w s capped $CAPPED"
}
scan A $LA &
p1=$!
scan B $LB &
p2=$!
wait $p1; wait $p2
cd $OUT
F=""
for P in A B; do [ -s scan_hi_D${D}_$P.jsonl ] && F="$F${F:+,}$WOUT/scan_hi_D${D}_$P.jsonl"; done
if [ -n "$F" ]; then
  "$PY" $Q/d18d_read.py $D $WTM $F > read_hi_D$D.log 2>&1
  echo "read_hi_D$D: exit $?: $(grep -E '^robust sign changes' read_hi_D$D.log); $(grep -E '^repeated points' read_hi_D$D.log)" >> $SUM
  "$PY" $Q/d18d_read.py $D $WTM $WMID/scan_D${D}_A.jsonl,$WMID/scan_D${D}_B.jsonl,$F > read_all_D$D.log 2>&1
  echo "read_all_D$D (1.70 to 2.35, d18mid's two files and these): exit $?: $(grep -E '^robust sign changes' read_all_D$D.log); $(grep -E '^repeated points' read_all_D$D.log)" >> $SUM
fi
"$PY" $WOUT/points_table_hi.py $WOUT > points_hi_D$D.md 2>&1
echo "points_table_hi: exit $?" >> $SUM
log "done"; echo "d18hi done" >> $SUM
touch $OUT/all.done
exit 0
