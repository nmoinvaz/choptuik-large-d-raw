#!/usr/bin/env bash
# #1025 D 17 k_c 71 (the coordinator's hc ~03:57 and ~04:01 UTC 21 Nov): the hybrid root on the Mac's float64 k_c 71 state at D 17 (raw I1025-mac/out/sol_l1kc71Fm1025_D17.0000.npy) by
# raw I1025-mac/p4_hybrid.py on the stub of its record (guess 2.0392799, README.md), then signtest.py at lam -/+ 0.02, then d17_verdict.py (P4 rules, outer-edge rule, signtest, k_c error).
# Code worktree D:/choptuik-1025p4 (505d8399), python venv-md510, 4 threads, BelowNormal (set by launch_d17.ps1; children inherit). Caps by exact pid after a command-line check
# (taskkill /T /F, not retried): hybrid 43200 s, signtest 10800 s. One line per event in ../exits_1025.txt. usage: bash d17_hybrid.sh
X=/d/choptuik-large-d-raw/I1025-win2b; WX=D:/choptuik-large-d-raw/I1025-win2b; D=$X/d17; WD=$WX/d17
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
PS2=$WX/rootpidpat.ps1
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
cd $D || exit 9
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "d17 not started: $WT is not at 505d8399"; exit 9; }
chk() { [ "$(git hash-object --no-filters $D/in/$1)" = "$2" ] || { log "d17 not started: in/$1 is not blob ${2:0:8}"; exit 9; }; }
chk p4_hybrid.py a402559b5d37661b49da50f07f877af21fd29b3a; chk signtest.py 179ea09681b0a75f7cefdff98984b48051b3f085; chk d18_check.py 08969ea28fbd6cb0d83e17c2d4ded1901ce6b209
chk sol_l1kc71Fm1025_D17.0000.npy 9e9f007ec5f5e1a038ff119b82d576e8748dd8a5; chk l1kc71Fm1025.jsonl d786d48948f75caef60f6b9163b9d80270041148
chk stub_l1kc71Fm1025_D17_guess2.0392799.jsonl 80b7ffde29d19fd94a3ba8fdd89138c808022eb0
for f in ell_p4_hybrid_1025_w_d17.jsonl hybrid_D17.log signtest_D17.log verdict_D17.log; do [ -e $D/$f ] && { log "d17 not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { log "d17 not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 MSYS2_ARG_CONV_EXCL='*'
export P4_WT_MATTER=$WTW/solver/matter P4_OUT=$WD/ell_p4_hybrid_1025_w_d17.jsonl
RC=0
runcap() { # name cap logfile script pat -- command...   (sets RC)
  local name=$1 cap=$2 lg=$3 script=$4 pat=$5; shift 6
  echo "== $name: $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $lg
  local t=$(date +%s) capped=0 wpid="" pid i cl
  "$@" >> $lg 2>&1 < /dev/null &
  pid=$!
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 3
    wpid=$(powershell -NoProfile -File "$PS2" -Script "$script" -Pat "$pat" | tr -d '\r')
    [ -n "$wpid" ] && break
    kill -0 $pid 2>/dev/null || break
  done
  if [ -n "$wpid" ]; then log "$name root pid $wpid, cap ${cap} s"
  elif kill -0 $pid 2>/dev/null; then log "UNEXPECTED: root pid of $name not found while it runs, no cap possible (left running)"
  else log "$name ended within seconds, no root pid taken"; fi
  while kill -0 $pid 2>/dev/null; do
    if [ -n "$wpid" ] && [ $(( $(date +%s) - t )) -ge $cap ]; then
      cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$wpid\").CommandLine" | tr -d '\r')
      case "$cl" in
        *"$script"*"$pat"*) log "$name CAP of ${cap} s reached, last log line: $(tail -n 1 $lg | cut -c1-160); killing the tree of pid $wpid"; MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1; capped=1;;
        *) log "pid $wpid is not the $name command (command line: ${cl:0:80}), nothing killed";;
      esac
      break
    fi
    sleep 15
  done
  wait $pid; RC=$?
  log "$name exit $RC wall $(( $(date +%s) - t ))s capped $capped"
  return 0
}
log "d17 chain starting: hybrid root on the Mac's k_c 71 D 17 state, guess 2.0392799 (inputs checked)"
ST=$WD/in/sol_l1kc71Fm1025_D17.0000.npy; STUB=$WD/in/stub_l1kc71Fm1025_D17_guess2.0392799.jsonl
runcap "hybrid kc71_D17" 43200 $D/hybrid_D17.log p4_hybrid.py stub_l1kc71Fm1025_D17 -- "$PYH" -u $WD/in/p4_hybrid.py $STUB $ST 17.0
line=$(tr -d '\r' < $D/hybrid_D17.log | grep -E "^D 17(\.0)? k_c 71 hybrid: lam" | tail -n 1)
if [ $RC = 0 ] && [ -n "$line" ] && ! echo "$line" | grep -q "lam None"; then
  log "d17 hybrid done: ${line:0:200}"
  cd $WT/solver/matter
  runcap "signtest kc71_D17" 10800 $D/signtest_D17.log signtest.py sol_l1kc71Fm1025_D17 -- "$PYH" -u $WD/in/signtest.py $ST 17.0 71 around=$P4_OUT:17.0:0.02
  "$PYH" $WD/d17_verdict.py $P4_OUT 17.0 $WD/signtest_D17.log $WD/in/d18_check.py "$PYH" < /dev/null 2>&1 | tr -d '\r' > $D/verdict_D17.log
  log "d17 verdict: $(grep -a '^VERDICT' $D/verdict_D17.log | tail -n 1)"
else
  log "d17 STOP: the hybrid row gave no root (exit $RC): ${line:0:200}"
fi
log "d17 chain done"
