#!/usr/bin/env bash
# #1033 runs 0-3 (coordinator's hc of 2026-11-19 ~18:00 UTC, to start after #945's M 384 record is posted): the commands of notes/LOW_D_SPEEDUP.md, 'Step 5, the measurement', 'Runs', from hp/ of the new worktree
# D:/choptuik-i1033 (branch perf/tau-map-lowd at 080acfa2, draft PR #1037). Run 0: selftest and its five controls. Run 1 (D 3.7): check, control gp, phase_gp (information), solve, report. Run 2: cost. Run 3 (D 3.0475): solve
# 1:384,0.4:192,0.5:192, then report. It stops after run 3 (no run 4).
# Differences from the note, all glue: the python of venv-i600 in place of python3 (its hpkernel read-only, nothing rebuilt), no `nice` (BelowNormal is set by the launching PowerShell and inherited), D:/ paths for the Windows python,
# each command's output in run1033.log, each exit code in exits_1033.txt. It writes the README first. It stops at the first exit code that is not the expected one (selftest 0, its controls 1, check 0, control gp 1, every solve 0,
# run 1's report 0, cost 0; phase_gp and run 3's report are recorded whatever they exit). Run 3's solve is capped at 3 h (10800 s) by the exact Windows pid of its python, after checking its command line.
# usage: bash run1033.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
CODE=/d/choptuik-i1033
RAW=/d/choptuik-large-d-raw
X=$RAW/I1033-win2
WRAW=D:/choptuik-large-d-raw
OUT=$WRAW/I1033-win2
L=$X/run1033.log
A=$WRAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475
S37=data/lowD_states/highm15_D3.7000
cap=10800
mkdir -p $X/states || exit 9
cd $CODE/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "1033 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1033.txt; }
G() { "$PY" -u tau_map_gain.py "$@"; }
stage() { # name expected-exit cmd...
  local name=$1 want=$2; shift 2
  echo "== $name: $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
  "$@" >> $L 2>&1
  local rc=$?
  log "$name exit $rc (expected $want)"
  if [ "$want" != any ] && [ "$rc" != "$want" ]; then log "UNEXPECTED exit at $name, stopping"; exit 1; fi
}
# README first
KF=$("$PY" -c "import hpkernel; print(hpkernel.__file__)" | tr -d '\r')
KD=$(dirname "$(cygpath -u "$KF")")
KS=$(sha256sum "$KD"/_hpkernel*.pyd | cut -c1-64)
{
printf '# I1033-win2: the tau-mapped grid at low D, measured (hp/tau_map_gain.py)\n\n'
printf 'win2, https://github.com/nmoinvaz/choptuik-large-d/issues/1033\n\n'
printf 'Runs 0-3 of notes/LOW_D_SPEEDUP.md, "Step 5, the measurement", "Runs" (coordinator, 2026-11-19), 8 threads at BelowNormal priority beside #1003.\n\n'
printf -- '- Code: worktree D:/choptuik-i1033, branch perf/tau-map-lowd (draft PR #1037) at %s, run from its hp/.\n' "$(git rev-parse --short=8 HEAD)"
printf -- '- hpkernel (read-only, the existing low-D venv, not rebuilt): `hpkernel.__file__` = %s\n' "$KF"
printf -- '  built as hpkernel-0.1.0 from main fc697f3a (fat LTO, worktree D:/choptuik-i600, #600; wheel D:/choptuik-i600/hp/dist/hpkernel-0.1.0-cp314-cp314-win_amd64.whl), `_hpkernel` .pyd sha256 %s\n' "$KS"
printf -- '- Python %s (venv-i600): numpy 2.5.4, mpmath 1.3.0, scipy 1.18.1, multidouble (Python package) 0.1.0.\n' "$("$PY" -c 'import sys; print(sys.version.split()[0])' | tr -d '\r')"
printf -- '- Inputs: RAW/T82-win/states (D 3.0475), RAW/T100-win2/states (D 3.044375), hp/data/lowD_states/highm15_D3.7000_M*.npz (D 3.7).\n'
printf -- '- Differences from the note: python of that venv for python3, no nice (priority set at launch), D:/ paths, output in run1033.log and exit codes in exits_1033.txt (launcher run1033.sh, glue only).\n'
printf -- '- Run 3 solve capped at 3 h by exact pid; no run 4 (the coordinator decides).\n\n'
printf 'Files: check37.jsonl, solve37.jsonl, report37.json (run 1); cost.jsonl (run 2); solve_D3.0475.jsonl, report_D3.0475.json (run 3); states/ (per-call checkpoints).\n'
} > $X/README.md
cp "$0" $X/run1033.sh
log "runs 0-3 start, code $(git rev-parse --short=8 HEAD), hpkernel $KF"
# run 0
stage "run0 selftest" 0 G selftest
for m in lo parity dps40 gp phase_gp; do stage "run0 selftest control $m" 1 G selftest --mutate $m; done
# run 1
stage "run1 check" 0 G check --threads 8 --out $OUT/check37.jsonl
stage "run1 check control gp" 1 G check --threads 8 --Ls 0.7 --mutate gp --out $OUT/check37.jsonl
stage "run1 check phase_gp (information)" any G check --threads 8 --Ls 0.7 --mutate phase_gp --out $OUT/check37.jsonl
stage "run1 solve" 0 G solve ${S37}_M128.npz --pairs 1:128,0.9:96,0.7:80,0.7:96,0.5:64,0.5:80,0.3:64,0.3:80 --threads 8 --states $OUT/states --out $OUT/solve37.jsonl
stage "run1 report" 0 G report $OUT/solve37.jsonl --ref ${S37}_M256.npz --uniform ${S37}_M128.npz --json $OUT/report37.json
# run 2
stage "run2 cost" 0 G cost --threads 8 --reps 2 --out $OUT/cost.jsonl
# run 3
echo "== run3 solve: ${A}_M384.npz --pairs 1:384,0.4:192,0.5:192 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $L
log "run3 solve start, cap ${cap} s"
t=$(date +%s)
G solve ${A}_M384.npz --pairs 1:384,0.4:192,0.5:192 --threads 8 --states $OUT/states --out $OUT/solve_D3.0475.jsonl >> $L 2>&1 &
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
[ "$rc" != 0 ] && { log "UNEXPECTED exit at run3 solve, stopping"; exit 1; }
stage "run3 report" any G report $OUT/solve_D3.0475.jsonl --ref ${A}_M384.npz --ref2 ${A}_M320.npz --cost $OUT/cost.jsonl --json $OUT/report_D3.0475.json
log "runs 0-3 done (no run 4)"
