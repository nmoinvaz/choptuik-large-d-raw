#!/usr/bin/env bash
# #1025 D 18.0625 hybrid sign scan ABOVE the first window, k_c 63 (the coordinator's hc ~16:00 UTC 21 Nov; README.md section "Part 2" written before the run). Same script, state and record as
# d18mid_driver.sh (xfkappa's d18_hybsign.py blob e089207a on sol_l1kc63Wm1025_D18.062500.npy and the leap record), lambda 1.95 to 2.35 at 0.01 (41 points), two processes
# (A: 1.95 then 1.96-2.15, 21 points; B: 1.95 again then 2.16-2.35, 21 points), 4 BLAS/rayon threads each, BelowNormal (set by launch_d18up.ps1, inherited), caps 28800 s each by exact pid after a
# command-line check (taskkill /T /F of the root pid, not retried). Then merge_up.py (the repeat check at 1.95, and the comparison with the first window's 1.95), winb's pinned reader
# (read_d18mid_1025.py, blob 017ae1da) and rate_up.py. One line per event in ../exits_1025.txt, prefix "1025 d18up".
# usage: bash d18up_driver.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/d18mid; WD=D:/choptuik-large-d-raw/I1025-win2b/d18mid
EX=$X/exits_1025.txt
log() { echo "1025 d18up $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
cd $D || exit 9
log "driver started, pre-checks"
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "not started: $WT is not at 505d8399"; exit 9; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py || { log "not started: the worktree's solver code differs from 505d8399"; exit 9; }
while read -r b p; do
  [ "$(git hash-object --no-filters $D/in/$(basename $p))" = "$b" ] || { log "not started: in/$(basename $p) is not blob ${b:0:8}"; exit 9; }
done < $D/in/pins.txt
[ "$(git hash-object --no-filters $D/scan_merged.jsonl)" = 8b0c3bfc01d19768df4a20de2e2f0d8017887089 ] || { log "not started: scan_merged.jsonl (the first window's scan) is not blob 8b0c3bfc"; exit 9; }
for f in up_scanA.jsonl up_scanB.jsonl up_scan_merged.jsonl up_scanA_raw.log up_scanB_raw.log up_scanA.log up_scanB.log up_merge.log up_reading.log up_rate.log up_samples.csv up_rc_A up_rc_B; do [ -e $D/$f ] && { log "not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, multidouble; multidouble.dd_logdet" || { log "not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
"$PYH" -c "
import json
r=[json.loads(l) for l in open('$WD/in/l1kc63Wm1025.jsonl') if l.strip() and json.loads(l).get('D')==18.0625]
assert r and abs(r[-1]['F']-2.6753918623791614e-10)<1e-20 and r[-1]['steps']==2540, r
" || { log "not started: no D 18.0625 record line (F 2.6753918623791614e-10, 2540 steps) in the leap record"; exit 9; }
"$PYH" $WD/plant_checks_up.py "$PYH" $WD/in $WD < /dev/null 2>&1 | tr -d '\r' > $D/plant_checks_up_run.log
grep -aq "^plant_checks_up passes" $D/plant_checks_up_run.log || { log "not started: the planted controls of merge_up, rate_up and the reader fail (plant_checks_up_run.log)"; exit 9; }
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
LA=$("$PYH" -c 'print(",".join(["1.95"] + [f"{1.95 + 0.01 * i:.2f}" for i in range(1, 21)]))' | tr -d '\r')
LB=$("$PYH" -c 'print(",".join(["1.95"] + [f"{1.95 + 0.01 * i:.2f}" for i in range(21, 41)]))' | tr -d '\r')
log "lambda lists: A $LA ; B $LB"
# passive sampler (cpu, memory) of this driver's own scan processes only (the pattern is this folder's path), ended by its exact pid after the scans
powershell -NoProfile -ExecutionPolicy Bypass -File $WD/sample_d18mid.ps1 -Out $WD/up_samples.csv -Interval 60 -Pat 'I1025-win2b/d18mid/in/d18_hybsign.py' > /dev/null 2>&1 < /dev/null &
spid=$!; swin=$(cat /proc/$spid/winpid); log "sampler pid $swin (every 60 s, up_samples.csv)"
HS=$WD/in/d18_hybsign.py; REC=$WD/in/l1kc63Wm1025.jsonl; ST=$WD/in/sol_l1kc63Wm1025_D18.062500.npy
crun "scanA" 0 28800 d18_hybsign.py $D/up_scanA_raw.log $D/up_rc_A "$PYH" -u $HS $REC $ST 18.0625 $LA $WD/up_scanA.jsonl &
p1=$!
crun "scanB" 0 28800 d18_hybsign.py $D/up_scanB_raw.log $D/up_rc_B "$PYH" -u $HS $REC $ST 18.0625 $LB $WD/up_scanB.jsonl &
p2=$!
wait $p1 $p2
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$swin\").CommandLine" | tr -d '\r')
case "$cl" in *sample_d18mid.ps1*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $swin > /dev/null 2>&1; log "sampler pid $swin ended";; *) log "sampler pid $swin not ended (command line: ${cl:0:60})";; esac
for k in A B; do grep -a -vE 'Warning|^  [a-z]+ = ' $D/up_scan${k}_raw.log | tr -d '\r' > $D/up_scan$k.log; done
read rca capa < $D/up_rc_A; read rcb capb < $D/up_rc_B
if [ "$rca" != 0 ] || [ "$rcb" != 0 ]; then log "STOP: a scan process did not finish (A exit $rca capped $capa, B exit $rcb capped $capb; 3 = not the record system), no merge, no reading"; log "done"; exit 1; fi
"$PYH" $WD/merge_up.py $WD/up_scanA.jsonl $WD/up_scanB.jsonl $WD/up_scan_merged.jsonl $WD/scan_merged.jsonl < /dev/null 2>&1 | tr -d '\r' > $D/up_merge.log
log "merge: $(grep -a 'REPEAT CHECK at' $D/up_merge.log | cut -c1-200 | tail -n 1 | sed 's/.*-> //') ; $(grep -a 'PRIOR SCAN' $D/up_merge.log | sed 's/.*-> //' | cut -c1-80) ; $(grep -a '^merged\|no merged\|missing' $D/up_merge.log | tail -n 1)"
if [ -s $D/up_scan_merged.jsonl ]; then
  "$PYH" $WD/in/read_d18mid_1025.py $WD/up_scan_merged.jsonl < /dev/null 2>&1 | tr -d '\r' > $D/up_reading.log
  "$PYH" $WD/rate_up.py $WD/up_scan_merged.jsonl < /dev/null 2>&1 | tr -d '\r' > $D/up_rate.log
  log "reading: $(grep -a '^change in\|^no change\|local minimum\|^two robust' $D/up_reading.log | cut -c1-120 | tr '\n' '|' | cut -c1-600)"
  log "rate: $(grep -a '^plus-to-minus\|^RATE' $D/up_rate.log | cut -c1-260 | tr '\n' '|' | cut -c1-700)"
else
  log "STOP: no merged scan (the repeat check or a missing point), no reading"
fi
log "done"
