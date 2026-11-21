#!/usr/bin/env bash
# #1025 D 17 k_c 71, the dd M sign check (the coordinator's hc ~06:46 UTC 21 Nov; README.md "The dd M sign check"): modelled on raw I1025-win2/d18/run_d18.sh. From solver/matter of D:/choptuik-i1025d
# (wip/ell1-highD 48c36355, read only), venv-md510's python, 20 BLAS threads, BelowNormal (set by launch_d17dd.ps1; children inherit). (1) ell_ddm.py selftest (exit 0), (2) selftest --mutate=slices (exit 1),
# each capped 1800 s; then (3) ell_ddm.py det at 2.0200263141 and at 2.0600263141 in parallel, --noise 1e-24,1e-20,1e-16, capped 10800 s each. Caps by exact root pid after a command-line check
# (taskkill /T /F, not retried). One line per event in ../../exits_1025.txt. usage: bash d17_dd.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/d17; O=$D/dd; WO=D:/choptuik-large-d-raw/I1025-win2b/d17/dd
EX=$X/exits_1025.txt
log() { echo "1025 d17dd $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
W=/d/choptuik-i1025d
STATE=D:/choptuik-large-d-raw/I1025-win2b/d17/in/sol_l1kc71Fm1025_D17.0000.npy
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md510 OPENBLAS_NUM_THREADS=20 OMP_NUM_THREADS=20 MKL_NUM_THREADS=20
export PATH="/c/Users/nathan/Source/venv-md510/Scripts:$PATH"
cd $W/solver/matter || { log "not started: no $W/solver/matter"; exit 9; }
[ "$(git -C $W rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "not started: $W is not at 48c36355"; exit 9; }
[ "$(git hash-object --no-filters $D/in/sol_l1kc71Fm1025_D17.0000.npy | cut -c1-8)" = 9e9f007e ] || { log "not started: the state is not blob 9e9f007e"; exit 9; }
for f in selftest.log selftest_slices.log det_lo.log det_hi.log ell_ddm_d17_lo.jsonl ell_ddm_d17_hi.jsonl; do [ -e $O/$f ] && { log "not started: $f exists"; exit 9; }; done
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
log "start: ell_ddm.py $(git hash-object --no-filters ell_ddm.py | cut -c1-8), python $PY, BLAS threads 20, state blob 9e9f007e"
crun selftest 0 1800 ell_ddm.py $O/selftest.log $O/rc_selftest "$PY" -u ell_ddm.py selftest
crun selftest_slices 1 1800 ell_ddm.py $O/selftest_slices.log $O/rc_slices "$PY" -u ell_ddm.py selftest --mutate=slices
r1=$(cut -d' ' -f1 $O/rc_selftest); r2=$(cut -d' ' -f1 $O/rc_slices)
if [ "$r1" != 0 ] || [ "$r2" != 1 ]; then log "STOP: selftests not as required (selftest exit $r1 want 0, slices exit $r2 want 1)"; exit 1; fi
log "selftests as required; the two det points start in parallel"
crun det_lo 0 10800 ell_ddm.py $O/det_lo.log $O/rc_lo "$PY" -u ell_ddm.py det $STATE 17 71 2.0200263141 --noise 1e-24,1e-20,1e-16 --out $WO/ell_ddm_d17_lo.jsonl &
p1=$!
crun det_hi 0 10800 ell_ddm.py $O/det_hi.log $O/rc_hi "$PY" -u ell_ddm.py det $STATE 17 71 2.0600263141 --noise 1e-24,1e-20,1e-16 --out $WO/ell_ddm_d17_hi.jsonl &
p2=$!
wait $p1 $p2
"$PY" $WO/read_d17_dd.py $WO/ell_ddm_d17_lo.jsonl $WO/ell_ddm_d17_hi.jsonl < /dev/null 2>&1 | tr -d '\r' > $O/d17_dd_read.log
log "dd reading: $(tail -n 1 $O/d17_dd_read.log | cut -c1-200)"
log "done"
