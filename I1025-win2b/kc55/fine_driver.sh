#!/usr/bin/env bash
# #1025 D 18.5 finer hybrid sign scan at k_c 55, lambda 1.660 to 1.700 at 0.002 (the coordinator's hc ~22:26 UTC 21 Nov; README.md "Part 2" written before the run). The same script, state and record
# as kc55_driver.sh: xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unmodified) on the Mac's sol_l1kc55F1025_D18.500000.npy and its record line (the record system is checked first by the script:
# |F| within 1% and equal steps, else exit 3 and the driver stops). 21 points, two processes (A: 1.680 then 1.660-1.678, 11 evaluations; B: 1.680 again then 1.682-1.700, 11 evaluations), 4 BLAS/rayon
# threads each, BelowNormal (set by launch_fine.ps1, inherited), caps 28800 s each by exact pid after a command-line check (taskkill /T /F of the root pid, not retried). Then merge_fine.py (the repeat check
# at 1.680, the comparison with the 0.01 scan at 1.660, 1.680 and 1.700) and read_fine.py (the coordinator's reading). One line per event in ../exits_1025.txt, prefix "1025 kc55fine".
# usage: bash fine_driver.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/kc55; WD=D:/choptuik-large-d-raw/I1025-win2b/kc55
EX=$X/exits_1025.txt
log() { echo "1025 kc55fine $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
cd $D || exit 9
log "driver started, pre-checks"
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "not started: $WT is not at 505d8399"; exit 9; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py || { log "not started: the worktree's solver code differs from 505d8399"; exit 9; }
while read -r b p; do
  [ "$(git hash-object --no-filters $D/in/$(basename $p))" = "$b" ] || { log "not started: in/$(basename $p) is not blob ${b:0:8}"; exit 9; }
done < $D/in/pins.txt
[ "$(git hash-object --no-filters $D/scan_merged.jsonl)" = 24179d07661c86d192d397e39688fe6365a05ddf ] || { log "not started: scan_merged.jsonl (the 0.01 scan) is not blob 24179d07"; exit 9; }
for f in fine_scanA.jsonl fine_scanB.jsonl fine_scan_merged.jsonl fine_scanA_raw.log fine_scanB_raw.log fine_scanA.log fine_scanB.log fine_merge.log fine_reading.log fine_samples.csv fine_rc_A fine_rc_B; do [ -e $D/$f ] && { log "not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, multidouble; multidouble.dd_logdet" || { log "not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
"$PYH" -c "
import json
r=[json.loads(l) for l in open('$WD/in/l1kc55F1025.jsonl') if l.strip() and json.loads(l).get('D')==18.5]
assert len(r)==1 and r[-1]['kc']==55 and abs(r[-1]['F']-2.6618688406954084e-10)<1e-20 and r[-1]['steps']==2149, r
" || { log "not started: no single D 18.5 record line (k_c 55, F 2.6618688406954084e-10, 2149 steps) in the record"; exit 9; }
"$PYH" $WD/plant_checks_fine.py "$PYH" $WD/in $WD < /dev/null 2>&1 | tr -d '\r' > $D/plant_checks_fine_run.log
grep -aq "^plant_checks_fine passes" $D/plant_checks_fine_run.log || { log "not started: the planted controls of merge_fine and read_fine fail (plant_checks_fine_run.log)"; exit 9; }
log "pre-checks ok: pins, worktree 505d8399, record line, planted controls pass"
crun() {   # name want cap_s regex out-log rcfile cmd...: runs cmd in the background, kills only its root pid's tree when the cap passes and its command line matches the regex
  local name=$1 want=$2 cap=$3 rx=$4 lg=$5 rcf=$6; shift 6
  local t=$(date +%s) capped=0 pid wpid cl rc
  "$@" > $lg 2>&1 < /dev/null &
  pid=$!
  wpid=$(cat /proc/$pid/winpid)
  log "$name root pid $wpid, cap $cap s, want exit $want"
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *$rx*) log "$name cap $cap s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "$name pid $wpid does not match '$rx' (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid; rc=$?
  echo "exit $rc" >> $lg
  echo "$rc $capped" > $rcf
  log "$name exit $rc (want $want) wall $(( $(date +%s) - t )) s capped $capped $([ $rc = $want ] && echo OK || echo MISMATCH)"
}
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MSYS2_ARG_CONV_EXCL='*'
export P4_WT_MATTER=$WTW/solver/matter
LA=$("$PYH" -c 'print(",".join(["1.680"] + [f"{1.66 + 0.002 * i:.3f}" for i in range(0, 10)]))' | tr -d '\r')
LB=$("$PYH" -c 'print(",".join(["1.680"] + [f"{1.66 + 0.002 * i:.3f}" for i in range(11, 21)]))' | tr -d '\r')
log "lambda lists: A $LA ; B $LB"
powershell -NoProfile -ExecutionPolicy Bypass -File $WD/sample_kc55.ps1 -Out $WD/fine_samples.csv -Interval 60 -Pat 'I1025-win2b/kc55/in/d18_hybsign.py' > /dev/null 2>&1 < /dev/null &
spid=$!; swin=$(cat /proc/$spid/winpid); log "sampler pid $swin (every 60 s, fine_samples.csv)"
HS=$WD/in/d18_hybsign.py; REC=$WD/in/l1kc55F1025.jsonl; ST=$WD/in/sol_l1kc55F1025_D18.500000.npy
crun "scanA" 0 28800 d18_hybsign.py $D/fine_scanA_raw.log $D/fine_rc_A "$PYH" -u $HS $REC $ST 18.5 $LA $WD/fine_scanA.jsonl &
p1=$!
crun "scanB" 0 28800 d18_hybsign.py $D/fine_scanB_raw.log $D/fine_rc_B "$PYH" -u $HS $REC $ST 18.5 $LB $WD/fine_scanB.jsonl &
p2=$!
wait $p1 $p2
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$swin\").CommandLine" | tr -d '\r')
case "$cl" in *sample_kc55.ps1*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $swin > /dev/null 2>&1; log "sampler pid $swin ended";; *) log "sampler pid $swin not ended (command line: ${cl:0:60})";; esac
for k in A B; do grep -a -vE 'Warning|^  [a-z]+ = ' $D/fine_scan${k}_raw.log | tr -d '\r' > $D/fine_scan$k.log; done
read rca capa < $D/fine_rc_A; read rcb capb < $D/fine_rc_B
if [ "$rca" != 0 ] || [ "$rcb" != 0 ]; then log "STOP: a scan process did not finish (A exit $rca capped $capa, B exit $rcb capped $capb; 3 = not the record system), no merge, no reading"; log "done"; exit 1; fi
"$PYH" $WD/merge_fine.py 1.660 21 0.002 1.680 18.5 $WD/fine_scanA.jsonl $WD/fine_scanB.jsonl $WD/fine_scan_merged.jsonl $WD/scan_merged.jsonl < /dev/null 2>&1 | tr -d '\r' > $D/fine_merge.log
log "merge: $(grep -a 'REPEAT CHECK at' $D/fine_merge.log | tail -n 1 | sed 's/.*-> //' | cut -c1-20) ; prior scan: $(grep -a 'PRIOR SCAN' $D/fine_merge.log | sed 's/.*-> //' | cut -c1-12 | tr '\n' ' ') ; $(grep -a '^merged\|no merged\|missing' $D/fine_merge.log | tail -n 1 | cut -c1-100)"
if [ -s $D/fine_scan_merged.jsonl ]; then
  "$PYH" $WD/read_fine.py $WD/fine_scan_merged.jsonl --step 0.002 --ends -,- < /dev/null 2>&1 | tr -d '\r' > $D/fine_reading.log
  log "reading: $(grep -a '^change in\|^no change\|local minimum\|^endpoint\|^FINE READING' $D/fine_reading.log | cut -c1-170 | tr '\n' '|' | cut -c1-1200)"
else
  log "STOP: no merged scan (the repeat check or a missing point), no reading"
fi
log "done"
