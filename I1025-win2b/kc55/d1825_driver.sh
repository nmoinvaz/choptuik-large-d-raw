#!/usr/bin/env bash
# #1025 D 18.25 hybrid sign scan at k_c 55 (the k_c test; the coordinator's hc ~23:25 UTC 21 Nov; README.md "Part 3" written before the run). xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a,
# unmodified) on the Mac's sol_l1kc55F1025_D18.250000.npy (blob cbaffca8) and its record line (I1025-mac/out/l1kc55F1025.jsonl, the one D 18.25 line: F 2.777068169891278e-10, 2190 steps); the script checks the
# record system first (|F| within 1% and equal steps, else exit 3 and the driver stops). lambda 1.30 to 2.40 at 0.02 (56 points), two processes (A: 1.86 then 1.30-1.84, 29 evaluations; B: 1.86 again then
# 1.88-2.40, 28 evaluations), 4 BLAS/rayon threads each, BelowNormal (set by launch_d1825.ps1, inherited), caps 28800 s each by exact pid after a command-line check (taskkill /T /F of the root pid, not retried).
# Then merge_fine.py (the repeat check at 1.86), read_fine.py (its line "FINE READING" is the fine scan's rule and is not used here), kc_compare2.py (the k_c test against xfkappa's k_c 63 roots 1.3885, 1.7425, 2.3187)
# and dip_fit2.py (every ln|det| minimum without a change, with the dip fit). One line per event in ../exits_1025.txt, prefix "1025 kc55d1825".
# usage: bash d1825_driver.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/kc55; WD=D:/choptuik-large-d-raw/I1025-win2b/kc55
EX=$X/exits_1025.txt
log() { echo "1025 kc55d1825 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
cd $D || exit 9
log "driver started, pre-checks"
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "not started: $WT is not at 505d8399"; exit 9; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py || { log "not started: the worktree's solver code differs from 505d8399"; exit 9; }
while read -r b p; do
  [ "$(git hash-object --no-filters $D/in/$(basename $p))" = "$b" ] || { log "not started: in/$(basename $p) is not blob ${b:0:8}"; exit 9; }
done < $D/in/pins_d1825.txt
for f in d1825_scanA.jsonl d1825_scanB.jsonl d1825_scan_merged.jsonl d1825_scanA_raw.log d1825_scanB_raw.log d1825_scanA.log d1825_scanB.log d1825_merge.log d1825_reading.log d1825_compare.log d1825_dipfit.log d1825_samples.csv d1825_rc_A d1825_rc_B; do [ -e $D/$f ] && { log "not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, multidouble; multidouble.dd_logdet" || { log "not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
"$PYH" -c "
import json
r=[json.loads(l) for l in open('$WD/in/l1kc55F1025.jsonl') if l.strip() and json.loads(l).get('D')==18.25]
assert len(r)==1 and r[-1]['kc']==55 and abs(r[-1]['F']-2.777068169891278e-10)<1e-20 and r[-1]['steps']==2190, r
" || { log "not started: no single D 18.25 record line (k_c 55, F 2.777068169891278e-10, 2190 steps) in the record"; exit 9; }
"$PYH" $WD/plant_checks_d1825.py "$PYH" $WD < /dev/null 2>&1 | tr -d '\r' > $D/plant_checks_d1825_run.log
grep -aq "^plant_checks_d1825 passes" $D/plant_checks_d1825_run.log || { log "not started: the planted controls of kc_compare2, merge_fine, read_fine and dip_fit2 fail (plant_checks_d1825_run.log)"; exit 9; }
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
LA=$("$PYH" -c 'print(",".join(["1.86"] + [f"{1.30 + 0.02 * i:.2f}" for i in range(0, 28)]))' | tr -d '\r')
LB=$("$PYH" -c 'print(",".join(["1.86"] + [f"{1.30 + 0.02 * i:.2f}" for i in range(29, 56)]))' | tr -d '\r')
log "lambda lists: A $LA ; B $LB"
powershell -NoProfile -ExecutionPolicy Bypass -File $WD/sample_kc55.ps1 -Out $WD/d1825_samples.csv -Interval 60 -Pat 'I1025-win2b/kc55/in/d18_hybsign.py' > /dev/null 2>&1 < /dev/null &
spid=$!; swin=$(cat /proc/$spid/winpid); log "sampler pid $swin (every 60 s, d1825_samples.csv)"
HS=$WD/in/d18_hybsign.py; REC=$WD/in/l1kc55F1025.jsonl; ST=$WD/in/sol_l1kc55F1025_D18.250000.npy
crun "scanA" 0 28800 d18_hybsign.py $D/d1825_scanA_raw.log $D/d1825_rc_A "$PYH" -u $HS $REC $ST 18.25 $LA $WD/d1825_scanA.jsonl &
p1=$!
crun "scanB" 0 28800 d18_hybsign.py $D/d1825_scanB_raw.log $D/d1825_rc_B "$PYH" -u $HS $REC $ST 18.25 $LB $WD/d1825_scanB.jsonl &
p2=$!
wait $p1 $p2
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$swin\").CommandLine" | tr -d '\r')
case "$cl" in *sample_kc55.ps1*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $swin > /dev/null 2>&1; log "sampler pid $swin ended";; *) log "sampler pid $swin not ended (command line: ${cl:0:60})";; esac
for k in A B; do grep -a -vE 'Warning|^  [a-z]+ = ' $D/d1825_scan${k}_raw.log | tr -d '\r' > $D/d1825_scan$k.log; done
read rca capa < $D/d1825_rc_A; read rcb capb < $D/d1825_rc_B
if [ "$rca" != 0 ] || [ "$rcb" != 0 ]; then log "STOP: a scan process did not finish (A exit $rca capped $capa, B exit $rcb capped $capb; 3 = not the record system), no merge, no reading"; log "done"; exit 1; fi
"$PYH" $WD/merge_fine.py 1.30 56 0.02 1.86 18.25 $WD/d1825_scanA.jsonl $WD/d1825_scanB.jsonl $WD/d1825_scan_merged.jsonl $WD/no_prior_scan.jsonl < /dev/null 2>&1 | tr -d '\r' > $D/d1825_merge.log
log "merge: $(grep -a 'REPEAT CHECK at' $D/d1825_merge.log | tail -n 1 | sed 's/.*-> //' | cut -c1-20) ; $(grep -a '^merged\|no merged\|missing' $D/d1825_merge.log | tail -n 1 | cut -c1-100)"
if [ -s $D/d1825_scan_merged.jsonl ]; then
  "$PYH" $WD/read_fine.py $WD/d1825_scan_merged.jsonl --step 0.02 < /dev/null 2>&1 | tr -d '\r' > $D/d1825_reading.log
  "$PYH" $WD/kc_compare2.py $WD/d1825_scan_merged.jsonl --band 0.02 --r63 1.3885,1.7425,2.3187 --ori63 plus-to-minus,minus-to-plus,plus-to-minus --cov63 1.20,2.60 < /dev/null 2>&1 | tr -d '\r' > $D/d1825_compare.log
  "$PYH" $WD/dip_fit2.py $WD/d1825_scan_merged.jsonl --half 5 < /dev/null 2>&1 | tr -d '\r' > $D/d1825_dipfit.log
  log "reading: $(grep -a '^change in\|^no change\|local minimum\|^endpoint' $D/d1825_reading.log | cut -c1-150 | tr '\n' '|' | cut -c1-900)"
  log "compare: $(grep -a '^k_c 55 change\|^k_c 63 root\|^SUMMARY' $D/d1825_compare.log | cut -c1-170 | tr '\n' '|' | cut -c1-1200)"
  log "dip fit: $(grep -a 'WITHOUT a change\|^minimum\|^  l0' $D/d1825_dipfit.log | cut -c1-200 | tr '\n' '|' | cut -c1-600)"
else
  log "STOP: no merged scan (the repeat check or a missing point), no reading"
fi
log "done"
