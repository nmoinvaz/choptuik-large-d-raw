#!/usr/bin/env bash
# #1025 lambda at k_c 63, D 16.25, from win2b's own k_c 55 D 16.25 state (coordinator's hc ~10:19 UTC 20 Nov): from solver/matter of D:/choptuik-i1025b (wip/ell1-highD 5c9d001c), venv-i962, 4 BLAS threads, BelowNormal (set by the launching PowerShell):
#   ell_refine.py l1kc55Fu1025 55 l1kc63Fu1025 63 1 16.25 2.1974112 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60   -> data/l1kc63Fu1025.jsonl, data/sol_l1kc63Fu1025_D16.2500.npy, log kc63_D16.25.log
# The ordered 12 h cap is a cap on the job's tree by its exact pid (43200 s; taskkill /T /F after a command-line check), not retried. When the job exits with a record that has a lambda, its signtest runs (lambda -/+ 0.02, capped 7200 s by exact pid):
#   signtest.py data/sol_l1kc63Fu1025_D16.2500.npy 16.25 63 around=data/l1kc63Fu1025.jsonl:16.25:0.02   -> signtest_kc63.log
# usage: bash run1025d.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
WX=D:/choptuik-large-d-raw/I1025-win2b
PS1=$WX/rootpid1025.ps1
PS2=$WX/rootpidpat.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
cd $W || exit 9
for f in l1kc63Fu1025.jsonl sol_l1kc63Fu1025_D16.2500.npy; do [ -e data/$f ] && { log "kc63 D16.25 not started: data/$f exists"; exit 9; }; done
[ "$(git rev-parse --short=8 HEAD)" = 5c9d001c ] || { log "kc63 D16.25 not started: worktree is not at 5c9d001c"; exit 9; }
cmp -s data/sol_l1kc55Fu1025_D16.2500.npy $X/out/sol_l1kc55Fu1025_D16.2500.npy || { log "kc63 D16.25 not started: the k_c 55 D 16.25 state differs from the published out/ copy"; exit 9; }
echo "$(git hash-object data/sol_l1kc55Fu1025_D16.2500.npy) data/sol_l1kc55Fu1025_D16.2500.npy (win2b's own k_c 55 D 16.25 state, equal to out/)" > $X/kc63_hashes.txt
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
name=kc63_D16.25 tag=l1kc63Fu1025 cap=43200 lg=$X/kc63_D16.25.log
echo "== $name: ell_refine.py l1kc55Fu1025 55 l1kc63Fu1025 63 1 16.25 2.1974112 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
t=$(date +%s); capped=0; wpid=""
"$PY" -u ell_refine.py l1kc55Fu1025 55 l1kc63Fu1025 63 1 16.25 2.1974112 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $lg 2>&1 < /dev/null &
pid=$!
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
wait $pid; rc=$?
log "$name exit $rc wall $(( $(date +%s) - t ))s capped $capped"
[ "$capped" = 1 ] && exit 99
if [ -s data/l1kc63Fu1025.jsonl ] && grep -q '"lam": [0-9]' data/l1kc63Fu1025.jsonl; then
  echo "== signtest kc63 D16.25 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/signtest_kc63.log
  t2=$(date +%s); c2=0; w2=""
  "$PY" -u $WX/signtest.py data/sol_l1kc63Fu1025_D16.2500.npy 16.25 63 around=data/l1kc63Fu1025.jsonl:16.25:0.02 >> $X/signtest_kc63.log 2>&1 < /dev/null &
  p2=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    w2=$(powershell -NoProfile -File "$PS2" -Script signtest.py -Pat sol_l1kc63Fu1025_D16.2500.npy | tr -d '\r')
    [ -n "$w2" ] && break
    kill -0 $p2 2>/dev/null || break
  done
  while kill -0 $p2 2>/dev/null; do
    if [ $(( $(date +%s) - t2 )) -ge 7200 ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$w2\").CommandLine" | tr -d '\r')
      case "$cl" in
        *signtest.py*sol_l1kc63Fu1025*) log "signtest kc63 D16.25 CAP of 7200 s reached, killing the tree of pid $w2"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $w2 > /dev/null 2>&1; c2=1;;
        *) log "pid $w2 is not the kc63 signtest, nothing killed";;
      esac
      break
    fi
    sleep 10
  done
  wait $p2; r2=$?
  log "signtest kc63 D16.25 exit $r2 wall $(( $(date +%s) - t2 ))s capped $c2"
else
  log "$name: no record with a lambda, no signtest"
fi
