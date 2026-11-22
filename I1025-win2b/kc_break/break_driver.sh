#!/usr/bin/env bash
# #1025 where the k_c-stable branch of lambda_1 breaks: the hybrid sign scans at D 18.375 at k_c 63 and k_c 55 (the coordinator's hc ~02:50 UTC 22 Nov; README.md written before the run). xfkappa's d18_hybsign.py
# (raw I1025-mac/d18, blob e089207a, unmodified) on the Mac's sol_l1kc63Wm1025_D18.375000.npy with its leap record line (I1025-mac/d18/l1kc63Wm1025.jsonl) and on sol_l1kc55F1025_D18.375000.npy with its record line
# (I1025-mac/out/l1kc55F1025.jsonl); each script checks the record system first (|F| within 1% and equal steps, else exit 3 and the driver stops). lambda 1.62 to 1.80 at 0.01 (19 points) and then 1.71 again, one process
# per k_c, side by side, 4 BLAS/rayon threads each, BelowNormal (set by launch_break.ps1, inherited), caps 28800 s each by exact pid after a command-line check (taskkill /T /F of the root pid, not retried). Then
# merge_repeat.py (the repeat check at 1.71, per k_c), read_fine.py (step 0.01), kc_break_compare.py (the coordinator's reading) and dip_fit3.py (every ln|det| minimum without a change, with the dip fit).
# One line per event in ../exits_1025.txt, prefix "1025 kcbreak".   usage: bash break_driver.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/kc_break; WD=D:/choptuik-large-d-raw/I1025-win2b/kc_break
EX=$X/exits_1025.txt
log() { echo "1025 kcbreak $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
cd $D || exit 9
log "driver started, pre-checks"
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "not started: $WT is not at 505d8399"; exit 9; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py || { log "not started: the worktree's solver code differs from 505d8399"; exit 9; }
while read -r b p; do
  [ "$(git hash-object --no-filters $D/in/$(basename $p))" = "$b" ] || { log "not started: in/$(basename $p) is not blob ${b:0:8}"; exit 9; }
done < $D/in/pins.txt
for f in b63_scan.jsonl b55_scan.jsonl b63_scan_merged.jsonl b55_scan_merged.jsonl b63_raw.log b55_raw.log b63.log b55.log b63_merge.log b55_merge.log b63_reading.log b55_reading.log compare.log b63_dipfit.log b55_dipfit.log samples.csv rc_63 rc_55; do [ -e $D/$f ] && { log "not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, multidouble; multidouble.dd_logdet" || { log "not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
"$PYH" -c "
import json
for fn, kc, F, st in (('l1kc63Wm1025.jsonl', 63, 2.791072127489636e-10, 2483), ('l1kc55F1025.jsonl', 55, 2.743469379731208e-10, 2169)):
    r=[json.loads(l) for l in open('$WD/in/'+fn) if l.strip() and json.loads(l).get('D')==18.375]
    assert len(r)==1 and r[-1]['kc']==kc and abs(r[-1]['F']-F)<1e-20 and r[-1]['steps']==st, (fn, r)
" || { log "not started: no single D 18.375 record line (k_c 63: F 2.791072127489636e-10, 2483 steps; k_c 55: F 2.743469379731208e-10, 2169 steps)"; exit 9; }
"$PYH" $WD/plant_checks_break.py "$PYH" $WD < /dev/null 2>&1 | tr -d '\r' > $D/plant_checks_break_run.log
grep -aq "^plant_checks_break passes" $D/plant_checks_break_run.log || { log "not started: the planted controls of kc_break_compare, merge_repeat, read_fine and dip_fit3 fail (plant_checks_break_run.log)"; exit 9; }
log "pre-checks ok: pins, worktree 505d8399, both record lines, planted controls pass"
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
L=$("$PYH" -c 'print(",".join([f"{1.62 + 0.01 * i:.2f}" for i in range(19)] + ["1.71"]))' | tr -d '\r')
log "lambda list (both k_c): $L"
powershell -NoProfile -ExecutionPolicy Bypass -File $WD/sample_kc55.ps1 -Out $WD/samples.csv -Interval 60 -Pat 'I1025-win2b/kc_break/in/d18_hybsign.py' > /dev/null 2>&1 < /dev/null &
spid=$!; swin=$(cat /proc/$spid/winpid); log "sampler pid $swin (every 60 s, samples.csv)"
HS=$WD/in/d18_hybsign.py
crun "scan_kc63" 0 28800 d18_hybsign.py $D/b63_raw.log $D/rc_63 "$PYH" -u $HS $WD/in/l1kc63Wm1025.jsonl $WD/in/sol_l1kc63Wm1025_D18.375000.npy 18.375 $L $WD/b63_scan.jsonl &
p1=$!
crun "scan_kc55" 0 28800 d18_hybsign.py $D/b55_raw.log $D/rc_55 "$PYH" -u $HS $WD/in/l1kc55F1025.jsonl $WD/in/sol_l1kc55F1025_D18.375000.npy 18.375 $L $WD/b55_scan.jsonl &
p2=$!
wait $p1 $p2
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$swin\").CommandLine" | tr -d '\r')
case "$cl" in *sample_kc55.ps1*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $swin > /dev/null 2>&1; log "sampler pid $swin ended";; *) log "sampler pid $swin not ended (command line: ${cl:0:60})";; esac
for k in 63 55; do grep -a -vE 'Warning|^  [a-z]+ = ' $D/b${k}_raw.log | tr -d '\r' > $D/b$k.log; done
read rca capa < $D/rc_63; read rcb capb < $D/rc_55
if [ "$rca" != 0 ] || [ "$rcb" != 0 ]; then log "STOP: a scan process did not finish (k_c 63 exit $rca capped $capa, k_c 55 exit $rcb capped $capb; 3 = not the record system), no merge, no reading"; log "done"; exit 1; fi
for k in 63 55; do
  "$PYH" $WD/merge_repeat.py $WD/b${k}_scan.jsonl $WD/b${k}_scan_merged.jsonl 1.62 19 0.01 1.71 18.375 $k < /dev/null 2>&1 | tr -d '\r' > $D/b${k}_merge.log
  log "merge k_c $k: $(grep -a 'REPEAT CHECK at' $D/b${k}_merge.log | tail -n 1 | sed 's/.*-> //' | cut -c1-20) ; $(grep -a '^merged\|no merged\|missing' $D/b${k}_merge.log | tail -n 1 | cut -c1-100)"
done
if [ -s $D/b63_scan_merged.jsonl ] && [ -s $D/b55_scan_merged.jsonl ]; then
  for k in 63 55; do
    "$PYH" $WD/read_fine.py $WD/b${k}_scan_merged.jsonl --step 0.01 < /dev/null 2>&1 | tr -d '\r' > $D/b${k}_reading.log
    "$PYH" $WD/dip_fit3.py $WD/b${k}_scan_merged.jsonl --half 5 < /dev/null 2>&1 | tr -d '\r' > $D/b${k}_dipfit.log
    log "reading k_c $k: $(grep -a '^change in\|^no change\|local minimum\|^endpoint' $D/b${k}_reading.log | cut -c1-150 | tr '\n' '|' | cut -c1-700)"
    log "dip fit k_c $k: $(grep -a 'WITHOUT a change\|^minimum\|^  l0' $D/b${k}_dipfit.log | cut -c1-220 | tr '\n' '|' | cut -c1-700)"
  done
  "$PYH" $WD/kc_break_compare.py $WD/b55_scan_merged.jsonl $WD/b63_scan_merged.jsonl --tol 0.01 < /dev/null 2>&1 | tr -d '\r' > $D/compare.log
  log "compare: $(grep -a '^k_c 6\|^k_c 5\|^PAIRING\|^NO k_c\|^READING\|^SUMMARY' $D/compare.log | cut -c1-260 | tr '\n' '|' | cut -c1-1500)"
else
  log "STOP: a scan did not merge (the repeat check or a missing point), no reading"
fi
log "done"
