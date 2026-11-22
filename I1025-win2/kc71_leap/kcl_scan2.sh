#!/bin/bash
# #1025 kc71_leap on win2: the hybrid scan of one D of the k_c 71 leap (the coordinator's hc of 2026-11-22 ~03:00 UTC): lambda LO to HI at 0.01 around the extrapolated path PATH, noise test and float64 sign, FOUR processes,
# 4 threads each, caps 28800 s by the exact root pids, xfkappa's d18_hybsign.py (blob e089207a). usage: kcl_scan.sh D LO HI PATH [WAIT_FILE]. It waits for the leap's saved state of D (copied into states/ by run_leap.sh's copier,
# at least 60 s old) and its record line, and for WAIT_FILE (the previous scan's .done) if given, so that the scans do not overlap. The points (n = (HI - LO) / 0.01 + 1) are split in four consecutive blocks (the first block takes
# the remainder); the pairs (P1, P2) and (P3, P4) each repeat the last point of the first block of the pair (c12, c34), evaluated first in both; the pair gate (pair_check2.py) compares them at the first points and kills all four scans by
# exact pid on a disagreement. Then kc71_leap_read.py (the reading) and points_table_leap.py.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
D=$1; LO=$2; HI=$3; PTH=$4; WAITF=${5:-}
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
RAWR=D:/choptuik-large-d-raw-push
Q=$RAWR/I1025-mac/d18
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
TAGL=${TAGL:-l1kc71Lw1025}
CAP=28800
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
DS=$("$PY" -c "print('%g' % float('$D'))")
DF=$("$PY" -c "print('%.6f' % float('$D'))")
DJ=$("$PY" -c "print(repr(float('$D')))")
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "D $DS refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2 "d18_hybsign.py"
for pr in "d18d_read.py 6b608903" "d185_scan_read.py 7c9d400f" "d18c_read.py 1383470f"; do set -- $pr; chk /d/choptuik-i935-raw/I1025-win2/d18mid/pinned/$1 $2 "pinned/$1"; done
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "D $DS refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "D $DS refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for i in 1 2 3 4; do [ -e $OUT/scan_D${DS}_P$i.jsonl ] && { log "D $DS refuse: scan_D${DS}_P$i.jsonl exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
cd $OUT
"$PY" kc71_leap_read.py --selftest > selftest_leapread.txt 2>&1; r1=$?
"$PY" kc71_leap_read.py --selftest --break > selftest_leapread_break.txt 2>&1; r2=$?
"$PY" pair_check2.py --selftest > selftest_pair2.txt 2>&1; p1=$?
"$PY" pair_check2.py --selftest --break > selftest_pair2_break.txt 2>&1; p2=$?
[ $r1 = 0 ] && [ $r2 = 1 ] && [ $p1 = 0 ] && [ $p2 = 1 ] || { log "D $DS: a control is wrong (leapread $r1/$r2 pair2 $p1/$p2): stop"; exit 1; }
log "D $DS scan waits for the state $OUT/states/sol_${TAGL}_D${DF}.npy ${WAITF:+and $WAITF}"
until [ -e $OUT/states/sol_${TAGL}_D${DF}.npy ] && [ $(( $(date +%s) - $(date -r $OUT/states/sol_${TAGL}_D${DF}.npy +%s) )) -ge 60 ] && grep -q "\"D\": $DJ," $OUT/states/${TAGL}.jsonl 2>/dev/null; do
  [ -e $OUT/${LEAPFIN:-leap.finished} ] && [ ! -e $OUT/states/sol_${TAGL}_D${DF}.npy ] && { echo "D $DS scan: the leap ended without the state of D $DS: no scan" >> $SUM; log "D $DS: the leap ended without the state: no scan"; touch $OUT/scan_D${DS}.done; exit 0; }
  sleep 30
done
if [ -n "$WAITF" ]; then until [ -e "$WAITF" ]; do sleep 30; done; fi
ST=$WOUT/states/sol_${TAGL}_D${DF}.npy
grep "\"D\": $DJ," $OUT/states/${TAGL}.jsonl | tail -n 1 > $OUT/rec_D${DS}.jsonl
REC=$WOUT/rec_D${DS}.jsonl
log "D $DS: state $(git hash-object --no-filters $OUT/states/sol_${TAGL}_D${DF}.npy | cut -c1-8), record $(git hash-object --no-filters $OUT/rec_D${DS}.jsonl | cut -c1-8): $(cut -c1-150 $OUT/rec_D${DS}.jsonl)"
"$PY" - "$LO" "$HI" "$DS" > $OUT/lists_D${DS}.txt <<'PYEOF'
import json, sys
lo, hi, ds = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
n = int(round((hi - lo) / 0.01)) + 1
g = [round(lo + 0.01 * i, 2) for i in range(n)]
base, extra = divmod(n, 4)
sizes = [base + (1 if i < extra else 0) for i in range(4)]
blocks, k = [], 0
for s in sizes:
    blocks.append(g[k:k + s]); k += s
c12, c34 = blocks[0][-1], blocks[2][-1]
lists = [blocks[0], [c12] + blocks[1], blocks[2], [c34] + blocks[3]]
lists[0] = [c12] + [x for x in blocks[0] if x != c12]
lists[2] = [c34] + [x for x in blocks[2] if x != c34]
json.dump(dict(c12=c12, c34=c34, n=n, sizes=sizes), open("D:/choptuik-i935-raw/I1025-win2/kc71_leap/checks_D%s.json" % ds, "w"))
for L in lists:
    print(",".join("%.2f" % x for x in L))
PYEOF
mapfile -t LISTS < $OUT/lists_D${DS}.txt
log "D $DS scan lists: P1 ${LISTS[0]} | P2 ${LISTS[1]} | P3 ${LISTS[2]} | P4 ${LISTS[3]}"
cd $WT/solver/matter || exit 1
scan() {  # P LAMS
  local P=$1 L=$2 s0=$(date +%s) rc w
  { echo "# $(date -u '+%F %T') UTC cmd: $PY -u $Q/d18_hybsign.py $REC $ST $DS $L $WOUT/scan_D${DS}_$P.jsonl (cwd $WTM, P4_WT_MATTER=$WTM, 4 threads)"; } > $OUT/scan_D${DS}_$P.log
  crun scanD${DS}_$P 0 $CAP d18_hybsign.py "$PY" -u $Q/d18_hybsign.py $REC $ST $DS $L $WOUT/scan_D${DS}_$P.jsonl >> $OUT/scan_D${DS}_$P.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $OUT/scan_D${DS}_$P.log
  local n; n=$(grep -c '^{' $OUT/scan_D${DS}_$P.jsonl 2>/dev/null); n=${n:-0}
  echo "scan_D${DS}_$P: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s"), $n points" >> $SUM
  log "scanD${DS}_$P exit $rc wall $w s capped $CAPPED"
}
killroot() {
  local pid; pid=$(grep " $1 root pid " $EX | tail -1 | sed -E 's/.* root pid ([0-9]+),.*/\1/')
  [ -n "$pid" ] || return
  local cl; cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$pid\").CommandLine" | tr -d '\r')
  case "$cl" in *d18_hybsign.py*) log "gate: killing the tree of $1 pid $pid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1;; *) log "gate: $1 pid $pid does not match d18_hybsign.py (${cl:0:60}), nothing killed";; esac
}
scan P1 ${LISTS[0]} &
q1=$!
scan P2 ${LISTS[1]} &
q2=$!
scan P3 ${LISTS[2]} &
q3=$!
scan P4 ${LISTS[3]} &
q4=$!
t0=$(date +%s); gate=none
while kill -0 $q1 2> /dev/null || kill -0 $q2 2> /dev/null || kill -0 $q3 2> /dev/null || kill -0 $q4 2> /dev/null; do
  "$PY" $OUT/pair_check2.py $WOUT $DS > $OUT/pair_check_D${DS}.txt 2>&1; g=$?
  if [ $g = 0 ]; then gate=pass; log "D $DS pair gate passed"; echo "D $DS pair gate: passed after $(( $(date +%s) - t0 )) s: $(grep '^PAIRS' $OUT/pair_check_D${DS}.txt)" >> $SUM; break; fi
  if [ $g = 1 ]; then gate=fail; log "D $DS pair gate FAILED: killing all four scans"; echo "D $DS pair gate: FAILED: $(grep -E 'DISAGREE' $OUT/pair_check_D${DS}.txt | head -n 2 | tr '\n' ' ')" >> $SUM; for n in P1 P2 P3 P4; do killroot scanD${DS}_$n; done; break; fi
  if [ $(( $(date +%s) - t0 )) -gt 7200 ]; then gate=fail; log "D $DS pair gate: no first points after 7200 s; killing all four scans"; echo "D $DS pair gate: no first points after 7200 s" >> $SUM; for n in P1 P2 P3 P4; do killroot scanD${DS}_$n; done; break; fi
  sleep 30
done
[ $gate = none ] && { gate=fail; echo "D $DS pair gate: the scans ended before the first points were compared" >> $SUM; }
wait $q1; wait $q2; wait $q3; wait $q4
cd $OUT
if [ $gate = pass ]; then
  "$PY" kc71_leap_read.py $WOUT $DS $PTH > read_D${DS}.txt 2>&1
  echo "D $DS kc71_leap_read: exit $?: $(grep -E '^(LAMBDA_1|NOT READ|STOP-level)' read_D${DS}.txt | cut -c1-260)" >> $SUM
fi
"$PY" points_table_leap.py $WOUT $DS > points_D${DS}.md 2>&1
log "D $DS scan done (gate $gate)"; echo "D $DS scan done (pair gate $gate)" >> $SUM
touch $OUT/scan_D${DS}.done
exit 0
