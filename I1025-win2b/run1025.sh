#!/usr/bin/env bash
# #1025 lambda_1 at k_c 55, D 16.25 and 16.75, from the k_c 47 leap states (coordinator's hc of 2026-11-20 ~06:45 UTC, commands from xfkappa): from solver/matter of the worktree D:/choptuik-i1025b (detached at origin/wip/ell1-highD 5c9d001c),
# venv-i962's python, 4 BLAS threads each, BelowNormal (set by the launching PowerShell and inherited). The two ell_refine.py runs start at once and write data/l1kc55Fv1025.jsonl + data/sol_l1kc55Fv1025_D16.7500.npy (D 16.75)
# and data/l1kc55Fu1025.jsonl + data/sol_l1kc55Fu1025_D16.2500.npy (D 16.25) in that worktree; logs in this folder (kc55_D16.75.log, kc55_D16.25.log). The ordered cap is `timeout 43200` (12 h): here each job's venv launcher stub is found
# by rootpid1025.ps1 and at 43200 s its tree is killed by that exact pid (taskkill /T /F) after its command line is checked, so no orphaned python is left (timeout would kill the stub only). A cap that fires is logged with the last log line and not retried.
# The signtests are not in this script (planted control first, then one signtest per record, by hand). usage: bash run1025.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
PS1=D:/choptuik-large-d-raw/I1025-win2b/rootpid1025.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*ell_refine.py*' }).Count" | tr -d '\r')
[ "$n" = 0 ] || { log "not started: $n ell_refine python processes are alive"; exit 9; }
for f in l1kc55Fv1025.jsonl l1kc55Fu1025.jsonl sol_l1kc55Fv1025_D16.7500.npy sol_l1kc55Fu1025_D16.2500.npy; do [ -e $W/data/$f ] && { log "not started: data/$f exists"; exit 9; }; done
cd $W || exit 9
[ "$(git rev-parse --short=8 HEAD)" = 5c9d001c ] || { log "not started: worktree is not at 5c9d001c"; exit 9; }
case "$(git hash-object data/sol_l1kc47Fx1025_D16.7500.npy)" in 6c4d8278*) ;; *) log "not started: D 16.75 state hash differs"; exit 9;; esac
case "$(git hash-object data/sol_l1kc47Fx1025_D16.2500.npy)" in 4c169200*) ;; *) log "not started: D 16.25 state hash differs"; exit 9;; esac
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
runjob() { # name tag cap-seconds logfile ell_refine-args...
  local name=$1 tag=$2 cap=$3 lg=$4; shift 4
  echo "== $name: ell_refine.py $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" i
  "$PY" -u ell_refine.py "$@" >> $lg 2>&1 &
  local pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS1" -Pat "$tag" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  if [ -n "$wpid" ]; then echo "$wpid" > $X/${name}.winpid; log "$name root pid $wpid, cap ${cap} s"
  elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of $name not found while it runs, no cap possible (python left running)"; wait $pid; exit 1
  else log "$name ended within seconds, no root pid taken"; fi
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *ell_refine.py*$tag*) log "$name CAP of ${cap} s reached, last log line: $(tail -n 1 $lg | cut -c1-160); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
  [ "$capped" = 1 ] && exit 99
  exit $rc
}
log "start, worktree $(git rev-parse --short=8 HEAD), raw origin/main $(git -C /d/choptuik-large-d-raw-743p rev-parse --short=8 origin/main)"
runjob D16.75 l1kc55Fv1025 43200 $X/kc55_D16.75.log l1kc47Fx1025 47 l1kc55Fv1025 55 1 16.75 2.0928 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pa=$!
runjob D16.25 l1kc55Fu1025 43200 $X/kc55_D16.25.log l1kc47Fx1025 47 l1kc55Fu1025 55 1 16.25 2.2009 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pb=$!
wait $pa; ra=$?
wait $pb; rb=$?
log "jobs ended: D 16.75 exit $ra, D 16.25 exit $rb (99 = cap)"
