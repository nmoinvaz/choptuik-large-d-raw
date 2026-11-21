#!/bin/bash
# #1025 d18mid on win2 (the coordinator's hc of 2026-11-21 ~13:30 UTC, the follow-on after the #1064 precross_natural rungs): xfkappa's hybrid sign scan (I1025-mac/d18/d18_hybsign.py, blob e089207a) at D 18.0625 and D 18.1875
# (k_c 63, the leap's saved states and record), lambda 1.70 to 1.95 at 0.01 (26 points each), the noise test and the float64 sign beside, side by side, 4 threads each, BelowNormal (the caller sets it), each capped at 28800 s
# by the exact root pid (taskkill /T /F /PID after the command line is checked), venv-md510. Then xfkappa's reader (d18d_read.py, blob 6b608903) on each scan and gap_table.py.
# usage: run_d18mid.sh [WAIT_FILE]   (WAIT_FILE: the scans start when it exists, e.g. the precross_natural all.done)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/d18mid
. $OUT/lib_d18mid.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/d18mid
RAWR=D:/choptuik-large-d-raw-push
Q=$RAWR/I1025-mac/d18
WT=/d/choptuik-i1025d
WTM=D:/choptuik-i1025d/solver/matter
REC=$Q/l1kc63Wm1025.jsonl
CAP=28800
WAITF=${1:-}
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
declare -A BLOB=( [d18_hybsign.py]=e089207a61fbd98614716abd309571cbc4888db2 [d18d_read.py]=6b608903 [d185_scan_read.py]=7c9d400fd0966a35ac306b5495febb4ec4efe7da [d18c_read.py]=1383470feaa976e4185e423626a0d5fec328de86
                  [sol_l1kc63Wm1025_D18.062500.npy]=f2307f0e [sol_l1kc63Wm1025_D18.187500.npy]=3f06b92e [l1kc63Wm1025.jsonl]=08f4dbf3 )
bad=0
for f in "${!BLOB[@]}"; do
  h=$(git hash-object --no-filters /d/choptuik-large-d-raw-push/I1025-mac/d18/$f)
  case "$h" in ${BLOB[$f]}*) ;; *) log "refuse: $f is blob $h, not ${BLOB[$f]}"; bad=1;; esac
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py || { log "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py || { log "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for D in 18.0625 18.1875; do [ -e $OUT/scan_D$D.jsonl ] && { log "refuse: scan_D$D.jsonl exists (d18_hybsign appends)"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "pins checked: d18_hybsign e089207a, d18d_read 6b608903, d185_scan_read 7c9d400f, d18c_read 1383470f, states f2307f0e (D 18.0625) and 3f06b92e (D 18.1875), record 08f4dbf3, solver code = 505d8399, ell_delta = 48c36355 (worktree $(git -C $WT rev-parse --short HEAD)), venv-md510"
cd $OUT
"$PY" $Q/d18d_read.py selftest > selftest_read.txt 2>&1; r1=$?
"$PY" $Q/d18d_read.py selftest --mutate=orient > selftest_read_mutate.txt 2>&1; r2=$?
echo "controls: d18d_read selftest exit $r1 (0), --mutate=orient exit $r2 (1)" >> $SUM; log "controls reader selftest $r1/$r2"
[ $r1 = 0 ] && [ $r2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
if [ -n "$WAITF" ]; then
  log "waiting for $WAITF"
  while [ ! -e "$WAITF" ]; do sleep 30; done
  log "$WAITF exists: the scans start"
fi
L=$("$PY" -c 'print(",".join(f"{1.70 + 0.01 * i:.2f}" for i in range(26)))')
log "lambda list: $L"
cd $WT/solver/matter || exit 1
scan() {  # D
  local D=$1 s0=$(date +%s) rc w
  local ST=$Q/sol_l1kc63Wm1025_D$(printf '%.6f' $D).npy
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D$D.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_D$D.log
  crun scan_D$D 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $REC $ST $D $L $WOUT/scan_D$D.jsonl >> $OUT/scan_D$D.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D$D.log
  local n; n=$(grep -c '^{' $OUT/scan_D$D.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D$D: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n of 26 points" >> $SUM
  log "scan_D$D exit $rc wall $w s capped $CAPPED"
}
scan 18.0625 &
p1=$!
scan 18.1875 &
p2=$!
wait $p1; wait $p2
cd $OUT
for D in 18.0625 18.1875; do
  [ -s scan_D$D.jsonl ] || continue
  "$PY" $Q/d18d_read.py $D $WTM $WOUT/scan_D$D.jsonl > read_D$D.log 2>&1
  echo "read_D$D: exit $?: $(grep -E '^robust sign changes' read_D$D.log)" >> $SUM
done
"$PY" $WOUT/gap_table.py $WOUT > gap_table.md 2>&1
echo "gap_table: exit $?" >> $SUM
log "done"; echo "d18mid done" >> $SUM
touch $OUT/all.done
exit 0
