#!/usr/bin/env bash
# #1025 D 18, the upper root near lambda_1 at k_c 63 (the coordinator's hc ~07:30 UTC 21 Nov, approved 07:42; README.md written before the run). After the D 17 dd check has ended
# ("d17dd done" or "d17dd STOP" in ../exits_1025.txt):
#  (1) raw I1025-mac/p4_hybrid.py (blob a402559b, unmodified) on the stub of winb's D 18 record (guess 1.825: the w 0.02 grid 1.7885, 1.825, 1.8615 holds the upper root only), on winb's D 18 state;
#      worktree D:/choptuik-1025p4 (505d8399), venv-md510, 4 threads, BelowNormal (set by launch_d18.ps1), cap 21600 s by exact pid.
#  (2) d18_gate.py: P4 rules + the outer-grid-point edge rule (raw d18_check.py) + the root in the scan's bracket (1.800, 1.810). If it fails: stop and report.
#  (3) ell_ddm.py selftest (exit 0) and selftest --mutate=slices (exit 1), then ell_ddm.py det at root -/+ 0.005, two processes in parallel (--noise 1e-24,1e-20,1e-16), worktree D:/choptuik-i1025d
#      (48c36355, read only), venv-md510, 20 BLAS threads as at D 17, caps 21600 s each by exact pid (6 h, the coordinator's hc ~09:55 UTC 21 Nov, replacing 10800 s).
#  (4) read_d18_dd.py (winb's Amendment 3 reading with the offset 0.005).
# Caps: taskkill /T /F of the exact root pid after a command-line check, not retried. One line per event in ../exits_1025.txt. usage: bash d18_chain.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
X=/d/choptuik-large-d-raw/I1025-win2b; D=$X/d18; WD=D:/choptuik-large-d-raw/I1025-win2b/d18
EX=$X/exits_1025.txt
log() { echo "1025 d18 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $EX; }
PYH=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-1025p4; WTW=D:/choptuik-1025p4
W=/d/choptuik-i1025d
ST=$WD/in/sol_l1kc63W1025_D18.000000.npy; STUB=$WD/in/stub_l1kc63W1025_D18_guess1.825.jsonl; JS=$WD/ell_p4_hybrid_1025_w_d18.jsonl
cd $D || exit 9
log "chain waiting for the D 17 dd check to end"
for i in $(seq 1 1440); do
  grep -aqE "^1025 d17dd (done|STOP)" $EX && break      # start of line: this script's own log lines begin "1025 d18"
  sleep 30
done
grep -aqE "^1025 d17dd (done|STOP)" $EX || { log "STOP: the D 17 dd check did not end within 12 h, nothing started"; exit 9; }
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "not started: $WT is not at 505d8399"; exit 9; }
[ "$(git -C $W rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "not started: $W is not at 48c36355"; exit 9; }
chk() { [ "$(git hash-object --no-filters $D/in/$1)" = "$2" ] || { log "not started: in/$1 is not blob ${2:0:8}"; exit 9; }; }
chk p4_hybrid.py a402559b5d37661b49da50f07f877af21fd29b3a; chk d18_check.py 08969ea28fbd6cb0d83e17c2d4ded1901ce6b209
chk sol_l1kc63W1025_D18.000000.npy 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21; chk stub_l1kc63W1025_D18_guess1.825.jsonl cb45e95ecdda8a7760d9205d7df44bbda17d636f
for f in ell_p4_hybrid_1025_w_d18.jsonl hybrid_D18.log gate_D18.log dd/selftest.log dd/selftest_slices.log dd/det_lo.log dd/det_hi.log; do [ -e $D/$f ] && { log "not started: $f exists"; exit 9; }; done
"$PYH" -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { log "not started: $PYH lacks multidouble.dd_logdet"; exit 9; }
mkdir -p $D/dd
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
# ---- (1) the hybrid root
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 MSYS2_ARG_CONV_EXCL='*'
export P4_WT_MATTER=$WTW/solver/matter P4_OUT=$JS
log "start: hybrid root on winb's k_c 63 D 18 state, guess 1.825, 4 threads (the D 17 dd check has ended)"
crun "hybrid kc63_D18" 0 21600 p4_hybrid.py $D/hybrid_D18.log $D/rc_hybrid "$PYH" -u $WD/in/p4_hybrid.py $STUB $ST 18.0
line=$(tr -d '\r' < $D/hybrid_D18.log | grep -E "^D 18(\.0)? k_c 63 hybrid: lam" | tail -n 1)
read rch capch < $D/rc_hybrid
if [ "$rch" = 0 ] && [ -n "$line" ] && ! echo "$line" | grep -q "lam None"; then
  log "hybrid done: ${line:0:200}"
else
  log "STOP: the hybrid row gave no root (exit $rch, capped $capch): ${line:0:200}"; log "done"; exit 1
fi
# ---- (2) the gate
"$PYH" $WD/d18_gate.py $JS $WD/in/d18_check.py "$PYH" < /dev/null 2>&1 | tr -d '\r' > $D/gate_D18.log
gl=$(grep -a '^GATE' $D/gate_D18.log | tail -n 1)
log "gate: ${gl:0:230}"
if ! echo "$gl" | grep -q "GATE D 18.0 k_c 63: PASS"; then log "STOP: a rule failed, the dd check is not run (reported, not read)"; log "done"; exit 1; fi
# ---- (3) the dd M sign check
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md510 OPENBLAS_NUM_THREADS=20 OMP_NUM_THREADS=20 MKL_NUM_THREADS=20
export PATH="/c/Users/nathan/Source/venv-md510/Scripts:$PATH"
set -- $("$PYH" -c "import json; r=[json.loads(l) for l in open('$JS') if l.strip()][-1]; print(repr(r['lam']), '%.10f' % round(r['lam']-0.005, 10), '%.10f' % round(r['lam']+0.005, 10))" | tr -d '\r')
ROOT=$1; LAMLO=$2; LAMHI=$3
log "dd check: root $ROOT, points $LAMLO and $LAMHI (root -/+ 0.005), 20 BLAS threads"
cd $W/solver/matter || { log "STOP: no $W/solver/matter"; exit 9; }
crun selftest 0 1800 ell_ddm.py $D/dd/selftest.log $D/dd/rc_selftest "$PYH" -u ell_ddm.py selftest
crun selftest_slices 1 1800 ell_ddm.py $D/dd/selftest_slices.log $D/dd/rc_slices "$PYH" -u ell_ddm.py selftest --mutate=slices
r1=$(cut -d' ' -f1 $D/dd/rc_selftest); r2=$(cut -d' ' -f1 $D/dd/rc_slices)
if [ "$r1" != 0 ] || [ "$r2" != 1 ]; then log "STOP: the dd selftests are not as required (selftest exit $r1 want 0, slices exit $r2 want 1)"; log "done"; exit 1; fi
log "dd selftests as required; the two det points start in parallel"
crun det_lo 0 21600 ell_ddm.py $D/dd/det_lo.log $D/dd/rc_lo "$PYH" -u ell_ddm.py det $ST 18 63 $LAMLO --noise 1e-24,1e-20,1e-16 --out $WD/dd/ell_ddm_d18_lo.jsonl &
p1=$!
crun det_hi 0 21600 ell_ddm.py $D/dd/det_hi.log $D/dd/rc_hi "$PYH" -u ell_ddm.py det $ST 18 63 $LAMHI --noise 1e-24,1e-20,1e-16 --out $WD/dd/ell_ddm_d18_hi.jsonl &
p2=$!
wait $p1 $p2
# ---- (4) the reading
"$PYH" $WD/read_d18_dd.py $WD/dd/ell_ddm_d18_lo.jsonl $WD/dd/ell_ddm_d18_hi.jsonl $ROOT $JS 0.005 < /dev/null 2>&1 | tr -d '\r' > $D/dd/d18_dd_read.log
log "dd reading: $(grep -a '^DDREAD' $D/dd/d18_dd_read.log | tail -n 1 | cut -c1-220)"
log "done"
