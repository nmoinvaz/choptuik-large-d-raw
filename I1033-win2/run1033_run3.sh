#!/usr/bin/env bash
# #1033 run 3 only (coordinator's hc of 2026-11-19 ~18:40 UTC: "start run 3 as it is (cap 3 h by exact pid) ... run its report with --cost on the M 128-256 file you have ... do not rerun run 2 ... post run 3's report table on #1033 and stop there").
# The commands of run1033.sh's run 3 block, unchanged (D 3.0475: solve 1:384,0.4:192,0.5:192 from the stored M 384 state, then report with --ref M 384, --ref2 M 320, --cost cost.jsonl, which has M 128 to 256 only), from hp/ of D:/choptuik-i1033
# at 080acfa2, venv-i600, 8 threads, BelowNormal (set by the launching PowerShell). The python is started directly (not through a shell function), so $! and its winpid are the python's own; the 3 h cap (10800 s) kills its tree by that exact Windows pid after
# checking its command line. The report runs after the solve exits (also when a map did not converge, which is a result), not after a cap kill. No run 2, no run 4. README.md and run1033.sh are not rewritten.
# usage: bash run1033_run3.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
CODE=/d/choptuik-i1033
RAW=/d/choptuik-large-d-raw
X=$RAW/I1033-win2
WRAW=D:/choptuik-large-d-raw
OUT=$WRAW/I1033-win2
L=$X/run1033.log
A=$WRAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475
cap=10800
cd $CODE/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "1033 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1033.txt; }
echo "== run3 solve: ${A}_M384.npz --pairs 1:384,0.4:192,0.5:192 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
log "run3 solve start (run1033_run3.sh, after the coordinator's go), cap ${cap} s, code $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u tau_map_gain.py solve ${A}_M384.npz --pairs 1:384,0.4:192,0.5:192 --threads 8 --states $OUT/states --out $OUT/solve_D3.0475.jsonl >> $L 2>&1 &
pid=$!
wpid=$(cat /proc/$pid/winpid)
echo "$wpid" > $X/run3.winpid
capped=0
while kill -0 $pid 2>/dev/null; do
  if [ $(( $(date +%s) - t )) -ge $cap ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
    case "$cl" in
      *tau_map_gain.py*solve*) log "run3 cap of ${cap} s reached, killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
      *) log "pid $wpid is not the run 3 solve (command line: ${cl:0:80}), nothing killed";;
    esac
    break
  fi
  sleep 15
done
wait $pid
rc=$?
log "run3 solve exit $rc wall $(( $(date +%s) - t ))s capped $capped"
[ "$capped" = 1 ] && { log "run3 capped, stopping (no report)"; exit 1; }
echo "== run3 report: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
"$PY" -u tau_map_gain.py report $OUT/solve_D3.0475.jsonl --ref ${A}_M384.npz --ref2 ${A}_M320.npz --cost $OUT/cost.jsonl --json $OUT/report_D3.0475.json >> $L 2>&1
log "run3 report exit $? (cost.jsonl has M 128-256 only)"
log "run 3 done (no run 4)"
