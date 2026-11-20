#!/usr/bin/env bash
# #1025 restart of the D 16.25 solve only (coordinator's hc ~06:46 UTC: D 16.25 was stopped at 06:45:45 UTC for memory; restart after win2-build's rustc falls below 10 GiB or its build ended). Same command, worktree, threads, cap by exact pid as run1025.sh
# (43200 s from this restart), appended to the same log kc55_D16.25.log. usage: bash run1025b.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
PS1=D:/choptuik-large-d-raw/I1025-win2b/rootpid1025.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
n=$(powershell -NoProfile -File "$PS1" -Pat l1kc55Fu1025 | tr -d '\r')
[ -z "$n" ] || { log "restart not started: a D 16.25 solve is alive (pid $n)"; exit 9; }
for f in l1kc55Fu1025.jsonl sol_l1kc55Fu1025_D16.2500.npy; do [ -e $W/data/$f ] && { log "restart not started: data/$f exists"; exit 9; }; done
cd $W || exit 9
[ "$(git rev-parse --short=8 HEAD)" = 5c9d001c ] || { log "restart not started: worktree is not at 5c9d001c"; exit 9; }
case "$(git hash-object data/sol_l1kc47Fx1025_D16.2500.npy)" in 4c169200*) ;; *) log "restart not started: D 16.25 state hash differs"; exit 9;; esac
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
name=D16.25 tag=l1kc55Fu1025 cap=43200 lg=$X/kc55_D16.25.log
echo "== $name RESTART: ell_refine.py l1kc47Fx1025 47 l1kc55Fu1025 55 1 16.25 2.2009 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
t=$(date +%s); capped=0; wpid=""
"$PY" -u ell_refine.py l1kc47Fx1025 47 l1kc55Fu1025 55 1 16.25 2.2009 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $lg 2>&1 &
pid=$!
for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 3
  wpid=$(powershell -NoProfile -File "$PS1" -Pat "$tag" | tr -d '\r')
  [ -n "$wpid" ] && break
  kill -0 $pid 2>/dev/null || break
done
if [ -n "$wpid" ]; then echo "$wpid" > $X/${name}.winpid; log "$name RESTART root pid $wpid, cap ${cap} s"
elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of the $name restart not found while it runs, no cap possible (python left running)"; wait $pid; exit 1
else log "$name restart ended within seconds, no root pid taken"; fi
while kill -0 $pid 2>/dev/null; do
  if [ $(( $(date +%s) - t )) -ge $cap ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
    case "$cl" in
      *ell_refine.py*$tag*) log "$name restart CAP of ${cap} s reached, last log line: $(tail -n 1 $lg | cut -c1-160); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
      *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
    esac
    break
  fi
  sleep 15
done
wait $pid
rc=$?
log "$name restart exit $rc wall $(( $(date +%s) - t ))s capped $capped"
