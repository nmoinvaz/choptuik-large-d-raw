#!/usr/bin/env bash
# #1025 lambda_1 at k_c 63, D 15 and D 15.5, from the k_c 55 bar states (coordinator's hc of 2026-11-20): from solver/matter of the worktree D:/choptuik-i1025c (detached at origin/wip/ell1-highD d4f0f854),
# venv-i962's python (win2b's venv, read only: the coordinator named it), 4 BLAS threads each, BelowNormal (set by the launching PowerShell, inherited). The two ell_refine.py runs start at once and write
# data/l1kc63Fy1025.jsonl + data/sol_l1kc63Fy1025_D15.0000.npy (D 15) and data/l1kc63Fz1025.jsonl + data/sol_l1kc63Fz1025_D15.5000.npy (D 15.5) in that worktree; logs in this folder.
# The ordered 12 h cap is applied as in win2b's run1025.sh (same method, written for this folder): each job's venv launcher stub is found by rootpid1025.ps1 (win2b's helper, copied) and at 43200 s its tree is killed by that exact
# pid (taskkill /T /F) after its command line is checked, so no orphaned python is left. A cap that fires is logged with the last log line and not retried. The signtests are in signtest1025c.sh.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"   # the launching PowerShell gives bash no login PATH (the first launch at 08:35:25 UTC stopped on an empty process count for want of tr)
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025c/solver/matter
X=/d/choptuik-i935-raw/I1025-win2c
PS1=D:/choptuik-i935-raw/I1025-win2c/rootpid1025.ps1
log() { echo "1025c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025c.txt; }
n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*ell_refine.py*' -and (\$_.CommandLine -like '*l1kc63Fy1025*' -or \$_.CommandLine -like '*l1kc63Fz1025*') }).Count" | tr -d '\r')
[ "$n" = 0 ] || { log "not started: $n of my ell_refine python processes are alive"; exit 9; }
for f in l1kc63Fy1025.jsonl l1kc63Fz1025.jsonl sol_l1kc63Fy1025_D15.0000.npy sol_l1kc63Fz1025_D15.5000.npy; do [ -e $W/data/$f ] && { log "not started: data/$f exists"; exit 9; }; done
cd $W || exit 9
[ "$(git rev-parse --short=8 HEAD)" = d4f0f854 ] || { log "not started: worktree is not at d4f0f854"; exit 9; }
case "$(git hash-object data/sol_l1kc55Fb1025_D15.0000.npy)" in ad055605*) ;; *) log "not started: D 15 state hash differs"; exit 9;; esac
case "$(git hash-object data/sol_l1kc55Fb1025_D15.5000.npy)" in 990ccde2*) ;; *) log "not started: D 15.5 state hash differs"; exit 9;; esac
case "$(git hash-object data/l1kc55Fb1025.jsonl)" in 5be40af4*) ;; *) log "not started: l1kc55Fb1025.jsonl hash differs"; exit 9;; esac
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
  exit $rc
}
log "start, worktree $(git rev-parse --short=8 HEAD), raw origin/main $(git -C /d/choptuik-i935-raw rev-parse --short=8 origin/main) (fetched, no pull)"
runjob D15 l1kc63Fy1025 43200 $X/kc63_D15.log l1kc55Fb1025 55 l1kc63Fy1025 63 1 15 2.4210058 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pa=$!
runjob D15.5 l1kc63Fz1025 43200 $X/kc63_D15.5.log l1kc55Fb1025 55 l1kc63Fz1025 63 1 15.5 2.3387882 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pb=$!
wait $pa; ra=$?
wait $pb; rb=$?
# the records and states into out/ (after both jobs ended, so no live writer is copied)
mkdir -p $X/out && cp $W/data/l1kc63Fy1025.jsonl $W/data/l1kc63Fz1025.jsonl $W/data/sol_l1kc63F[yz]1025_D*.npy $X/out/ 2>/dev/null
log "jobs ended: D 15 exit $ra, D 15.5 exit $rb; outputs copied to out/ ($(ls $X/out | tr '\n' ' '))"
touch $X/jobs.done
