#!/usr/bin/env bash
# #1025 two lambda redos at once (coordinator's hc ~09:07 UTC 20 Nov, after the signtest batch showed that the k_c 55 D 16.5 value 2.1591248 is not a root): from solver/matter of D:/choptuik-i1025b (wip/ell1-highD 5c9d001c), venv-i962,
# 4 BLAS threads each, BelowNormal (set by the launching PowerShell). Two same-k_c refines of stored Mac states (taken by git show of choptuik-large-d-raw origin/main f731f843, hashes in redo_hashes.txt):
#   (1) ell_refine.py l1kc55Fb1025 55 l1kc55Fw1025 55 1 16.5 2.1500 ...   (guess between the passing k_c 47 2.1548215 and k_c 63 2.1454677)  -> data/l1kc55Fw1025.jsonl, sol_l1kc55Fw1025_D16.5000.npy, log kc55_D16.5_redo.log
#   (2) ell_refine.py l1kc47Fr1025 47 l1kc47Fw1025 47 1 17 2.0257187 ...  (guess at the passing k_c 55 value)                            -> data/l1kc47Fw1025.jsonl, sol_l1kc47Fw1025_D17.0000.npy, log kc47_D17_redo.log
# all with --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60. The ordered `timeout 43200` is a 43200 s cap on each job's tree by its exact pid (taskkill /T /F after a command-line check), as in run1025.sh; not retried.
# If ell_refine refuses a same-k_c refine the log shows its message (the code is not changed). usage: bash run1025c.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
PS1=D:/choptuik-large-d-raw/I1025-win2b/rootpid1025.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
cd $W || exit 9
for f in l1kc55Fw1025.jsonl l1kc47Fw1025.jsonl sol_l1kc55Fw1025_D16.5000.npy sol_l1kc47Fw1025_D17.0000.npy; do [ -e data/$f ] && { log "redo not started: data/$f exists"; exit 9; }; done
[ "$(git rev-parse --short=8 HEAD)" = 5c9d001c ] || { log "redo not started: worktree is not at 5c9d001c"; exit 9; }
case "$(git hash-object data/sol_l1kc55Fb1025_D16.5000.npy)" in 557bfff0*) ;; *) log "redo not started: k_c 55 D 16.5 state hash differs"; exit 9;; esac
case "$(git hash-object data/sol_l1kc47Fr1025_D17.0000.npy)" in 69a64bd5*) ;; *) log "redo not started: k_c 47 D 17 state hash differs"; exit 9;; esac
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
runjob() { # name tag cap-seconds logfile ell_refine-args...
  local name=$1 tag=$2 cap=$3 lg=$4; shift 4
  echo "== $name: ell_refine.py $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" i
  "$PY" -u ell_refine.py "$@" >> $lg 2>&1 < /dev/null &
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
log "redo start, worktree $(git rev-parse --short=8 HEAD), raw origin/main f731f843"
runjob redo55_D16.5 l1kc55Fw1025 43200 $X/kc55_D16.5_redo.log l1kc55Fb1025 55 l1kc55Fw1025 55 1 16.5 2.1500 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pa=$!
runjob redo47_D17 l1kc47Fw1025 43200 $X/kc47_D17_redo.log l1kc47Fr1025 47 l1kc47Fw1025 47 1 17 2.0257187 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 &
pb=$!
wait $pa; ra=$?
wait $pb; rb=$?
log "redo jobs ended: k_c 55 D 16.5 exit $ra, k_c 47 D 17 exit $rb (99 = cap)"
