#!/bin/bash
# #1025 d185map, window B split in two (the coordinator's hc of 2026-11-21 ~19:32 UTC: "split B now. Keep A running. Restart B as two processes"): B1 = lambda 1.55 (xfkappa's repeat), then 1.28 to 1.54 (28 evaluations);
# B2 = lambda 1.55 (the repeat again), then 1.00 to 1.27 (29 evaluations); 4 threads each, BelowNormal (the caller sets it), each capped at 28800 s by the exact root pid, the same repeat gate (repeat_check_b.py: both first points
# against xfkappa's, same sign, ln|det| within 1e-2; a disagreement kills both B scans by their exact root pids and stops). The first run's window A keeps running under run_d185map.sh; its B was stopped (README). The final
# reading (all of A, B1 and B2 with xfkappa's scans) is run after all three have ended.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
P0=/d/choptuik-i935-raw/I1025-win2/d185map
OUT=$P0/b_split
. $OUT/lib_bsplit.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/d185map/b_split
W0=D:/choptuik-i935-raw/I1025-win2/d185map
RAWR=D:/choptuik-large-d-raw-push
Q=$RAWR/I1025-mac/d18
WT=/d/choptuik-i1025d
WTM=D:/choptuik-i1025d/solver/matter
REC=$Q/l1kc63Wm1025.jsonl
ST=$Q/sol_l1kc63Wm1025_D18.500000.npy
CAP=28800
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
declare -A BLOB=( [d18_hybsign.py]=e089207a61fbd98614716abd309571cbc4888db2 [sol_l1kc63Wm1025_D18.500000.npy]=33c1a58b [l1kc63Wm1025.jsonl]=08f4dbf3 )
bad=0
for f in d18_hybsign.py sol_l1kc63Wm1025_D18.500000.npy l1kc63Wm1025.jsonl; do
  h=$(git hash-object --no-filters /d/choptuik-large-d-raw-push/I1025-mac/d18/$f)
  case "$h" in ${BLOB[$f]}*) ;; *) log "refuse: $f is blob $h, not ${BLOB[$f]}"; bad=1;; esac
done
# the local copies of xfkappa's D 18.5 scans and the sign-convention reference equal the raw files
for f in d185_scan_1025.jsonl d185_scanhi_1025.jsonl d185_scanup_1025.jsonl d18_refsign_1025.jsonl; do
  a=$(git hash-object --no-filters /d/choptuik-large-d-raw-push/I1025-mac/d18/$f); b=$(git hash-object --no-filters $P0/inputs/$f)
  [ "$a" = "$b" ] || { log "refuse: inputs/$f ($b) differs from the raw file ($a)"; bad=1; }
done
# the pinned reader copies (made at the d18mid scan start from the pinned blobs)
for pr in "d18d_read.py 6b608903" "d185_scan_read.py 7c9d400f" "d18c_read.py 1383470f"; do
  set -- $pr
  h=$(git hash-object --no-filters /d/choptuik-i935-raw/I1025-win2/d18mid/pinned/$1)
  case "$h" in $2*) ;; *) log "refuse: pinned/$1 is blob $h, not $2"; bad=1;; esac
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
git -C $WT diff --quiet 48c36355d1ba64de4e3112ed968fd6c034384551 -- solver/matter/ell_delta.py || { log "refuse: the worktree's ell_delta.py differs from 48c36355"; bad=1; }
for f in scan_B1.jsonl scan_B2.jsonl; do [ -e $OUT/$f ] && { log "refuse: $f exists (d18_hybsign appends)"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "pins checked: d18_hybsign e089207a, state 33c1a58b (D 18.5), record 08f4dbf3, the pinned readers d18d_read 6b608903 / d185_scan_read 7c9d400f / d18c_read 1383470f, solver code = 505d8399, ell_delta = 48c36355 (worktree $(git -C $WT rev-parse --short HEAD)), venv-md510"
cd $OUT
"$PY" $P0/repeat_check_b.py --selftest > selftest_repeat.txt 2>&1; c1=$?
"$PY" $P0/repeat_check_b.py --selftest --break > selftest_repeat_break.txt 2>&1; c2=$?
"$PY" D:/choptuik-i935-raw/I1025-win2/d18mid/pinned/d18d_read.py selftest > selftest_read.txt 2>&1; r1=$?
"$PY" D:/choptuik-i935-raw/I1025-win2/d18mid/pinned/d18d_read.py selftest --mutate=orient > selftest_read_mutate.txt 2>&1; r2=$?
echo "controls: repeat_check selftest exit $c1 (0), --break exit $c2 (1); d18d_read selftest exit $r1 (0), --mutate=orient exit $r2 (1)" >> $SUM; log "controls repeat_check $c1/$c2 reader $r1/$r2"
[ $c1 = 0 ] && [ $c2 = 1 ] && [ $r1 = 0 ] && [ $r2 = 1 ] || { log "a control is wrong: stop"; exit 1; }
LB1=$("$PY" -c 'print("1.55," + ",".join(f"{1.28 + 0.01 * i:.2f}" for i in range(27)))')
LB2=$("$PY" -c 'print("1.55," + ",".join(f"{1.00 + 0.01 * i:.2f}" for i in range(28)))')
log "lambda list B1 (28): $LB1"
log "lambda list B2 (29): $LB2"
cd $WT/solver/matter || exit 1
scan() {  # P LAMS
  local P=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $WOUT/scan_$P.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_$P.log
  crun scan_$P 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $REC $ST 18.5 $L $WOUT/scan_$P.jsonl >> $OUT/scan_$P.log 2>&1
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
scan B1 $LB1 &
p1=$!
scan B2 $LB2 &
p2=$!
t0=$(date +%s); gate=none
while kill -0 $p1 2> /dev/null || kill -0 $p2 2> /dev/null; do
  "$PY" $P0/repeat_check_b.py $WOUT/scan_B1.jsonl $WOUT/scan_B2.jsonl > $OUT/repeat_check.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "repeat gate passed"; echo "repeat gate: passed after $(( $(date +%s) - t0 )) s: $(grep '^REPEATS' $OUT/repeat_check.txt)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "repeat gate FAILED: a repeated point disagrees; killing both B scans"; echo "repeat gate: FAILED: $(grep -E 'DISAGREE' $OUT/repeat_check.txt | head -n 2 | tr '
' ' ')" >> $SUM; killroot scan_B1; killroot scan_B2; break; fi
  if [ $(( $(date +%s) - t0 )) -gt 2700 ]; then gate=fail; log "repeat gate: no first points after 2700 s; killing both B scans"; echo "repeat gate: no first points after 2700 s" >> $SUM; killroot scan_B1; killroot scan_B2; break; fi
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "repeat gate: both scans ended before the first points were compared" >> $SUM; }
wait $p1; wait $p2
log "done (gate $gate)"; echo "bsplit done (repeat gate $gate)" >> $SUM
touch $OUT/all.done
exit 0
