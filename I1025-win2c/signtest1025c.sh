#!/usr/bin/env bash
# #1025 signtests (the coordinator's hc of 2026-11-20): signtest.py (xfkappa's I1025-mac/signtest.py, blob a2f53a90, hash checked here) from solver/matter of D:/choptuik-i1025c, venv-i962, 4 BLAS threads, BelowNormal,
# one at a time, output appended to signtest.log.
#   bash signtest1025c.sh planted : the planted control, which must print agree, agree, DISAGREE (the script logs whether it did)
#   bash signtest1025c.sh y       : the D 15 record (data/l1kc63Fy1025.jsonl, state data/sol_l1kc63Fy1025_D15.0000.npy) at lam -/+ 0.02
#   bash signtest1025c.sh z       : the same for D 15.5 (data/l1kc63Fz1025.jsonl, data/sol_l1kc63Fz1025_D15.5000.npy)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
W=/d/choptuik-i1025c/solver/matter
X=/d/choptuik-i935-raw/I1025-win2c
cd $W || exit 9
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
log() { echo "1025c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025c.txt; }
case "$(git hash-object $X/signtest.py)" in a2f53a90*) ;; *) log "signtest.py hash differs from a2f53a90, not run"; exit 9;; esac
case "$1" in
  planted)
    echo "== signtest planted $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/signtest.log
    timeout 3600 "$PY" -u $X/signtest.py planted >> $X/signtest.log 2>&1; rc=$?
    r=$(tail -n 3 $X/signtest.log | grep -ao "agree\|DISAGREE" | tr '\n' ' ')
    log "signtest planted exit $rc, verdicts: $r (must be: agree agree DISAGREE)";;
  y|z)
    if [ "$1" = y ]; then tag=Fy D=15 DS=15.0000; else tag=Fz D=15.5 DS=15.5000; fi
    echo "== signtest $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/signtest.log
    timeout 7200 "$PY" -u $X/signtest.py data/sol_l1kc63${tag}1025_D${DS}.npy $D 63 around=data/l1kc63${tag}1025.jsonl:$D:0.02 >> $X/signtest.log 2>&1; rc=$?
    log "signtest $1 (D $D) exit $rc";;
esac
