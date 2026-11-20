#!/usr/bin/env bash
# #1025 signtests (coordinator's hc ~06:45 UTC, commands from xfkappa): from solver/matter of D:/choptuik-i1025b, venv-i962, 4 BLAS threads, BelowNormal (set by the launching PowerShell), one at a time, output appended to signtest.log.
#   bash signtest1025.sh planted   : the planted control, which must print agree, agree, DISAGREE (the script logs whether it did)
#   bash signtest1025.sh v         : signtest of the D 16.75 record at lam -/+ 0.02:  timeout 7200 signtest.py data/sol_l1kc55Fv1025_D16.7500.npy 16.75 55 around=data/l1kc55Fv1025.jsonl:16.75:0.02
#   bash signtest1025.sh u         : the same for D 16.25 (data/sol_l1kc55Fu1025_D16.2500.npy, data/l1kc55Fu1025.jsonl)
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025b/solver/matter
X=/d/choptuik-large-d-raw/I1025-win2b
cd $W || exit 9
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
case "$1" in
  planted)
    echo "== signtest planted $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/signtest.log
    timeout 3600 "$PY" -u $X/signtest.py planted >> $X/signtest.log 2>&1; rc=$?
    r=$(tail -n 3 $X/signtest.log | grep -ao "agree\|DISAGREE" | tr '\n' ' ')
    log "signtest planted exit $rc, verdicts: $r (must be: agree agree DISAGREE)";;
  v|u)
    if [ "$1" = v ]; then tag=Fv D=16.75; else tag=Fu D=16.25; fi
    echo "== signtest $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/signtest.log
    timeout 7200 "$PY" -u $X/signtest.py data/sol_l1kc55${tag}1025_D${D}00.npy $D 55 around=data/l1kc55${tag}1025.jsonl:$D:0.02 >> $X/signtest.log 2>&1; rc=$?
    log "signtest $1 (D $D) exit $rc";;
esac
