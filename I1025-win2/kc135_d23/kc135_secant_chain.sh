#!/bin/bash
# #1025 kc135_d23 on win2 (the coordinator's hc of 2026-11-26 22:38 UTC): "If the 12 h cap stops the secant, restart it at once on the narrowed bracket from its own records (--ends from them), without waiting for me, and report."
# This waiter watches the running secant (kc135_secant.sh, run 1: it touches secant/secant.done); when that run ended CAPPED, it computes the narrowed bracket with narrow.py from the scan rows and the secant's own records, and
# starts run 2 (and, if that one is capped too, runs 3 and 4 at most) with the same command (--tol=1e-5 --maxev=10, pins, cap 43200 s on the exact pid, --ends = the two ends of the narrowed bracket). Each restart is logged
# in secant/chain_events.txt (and reported by hand). A run that ended by tol, maxev or a non-robust interior point is not restarted.
# usage: kc135_secant_chain.sh
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc135_d23; WOUT=D:/choptuik-i935-raw/I1025-win2/kc135_d23
SEC=$OUT/secant; WSEC=$WOUT/secant; SUM=$SEC/summary_secant.txt; EV=$SEC/chain_events.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
SWT=/d/choptuik-i1025secant92; SWTM=D:/choptuik-i1025secant92/solver/matter
NEW=l1kc135win2d23; D=23.0; CAP=43200
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$SWTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a $EV; log "kc135 secant chain $*"; }
mkdir -p $SEC
"$PY" -I $OUT/narrow.py --selftest > $SEC/selftest_narrow.txt 2>&1 || { say "STOP: narrow.py selftest did not exit 0"; exit 2; }
"$PY" -I $OUT/narrow.py --selftest --mutate > /dev/null 2>&1; [ $? = 1 ] || { say "STOP: narrow.py --selftest --mutate did not exit 1"; exit 2; }
say "chain armed: narrow.py selftest 0 and its mutation 1; waiting for run 1 (secant.done)"
REC=$WOUT/${NEW}.jsonl; ST=$WOUT/sol_${NEW}_D23.0000.npy
N=1
while :; do
  flag=$SEC/run$N.done; [ $N = 1 ] && flag=$SEC/secant.done
  until [ -e $flag ]; do sleep 60; done
  last=$(grep -E "^kc135 secant" $SUM | tail -n 1)
  case "$last" in *CAPPED*) ;; *) say "run $N ended without the cap ($last): no restart"; exit 0;; esac
  [ $N -ge 4 ] && { say "run $N was capped too: the chain stops after four runs (report)"; exit 0; }
  N=$((N + 1))
  nr=$("$PY" -I $OUT/narrow.py sol_${NEW}_D23.0000.npy $D $WSEC/ends_run$N.jsonl 0.045 0.05 $WOUT/scan/scan_D23.0_p1.jsonl $WOUT/scan/scan_D23.0_p2.jsonl $WOUT/scan/scan_D23.0_p3.jsonl $WOUT/scan/scan_D23.0_p4.jsonl $WSEC/secant.jsonl | tail -n 1 | tr -d '\r')
  set -- $nr
  [ -n "${2:-}" ] || { say "STOP: no narrowed bracket from the records ($nr)"; exit 3; }
  LO=$1; HI=$2
  say "run $((N - 1)) was CAPPED: restart (run $N) on the narrowed bracket ($LO, $HI) with --ends from the records"
  cd $SWT/solver/matter || exit 1
  { echo "# $(date -u '+%F %T') UTC run $N cmd: $PY -u $SWTM/d18_secant.py run $REC $ST $D $LO $HI $WSEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=cd134e2c,bc295fbc --ends=$WSEC/ends_run$N.jsonl (cwd $SWTM, 1 thread, Normal)"; } > $SEC/secant_run$N.log
  s0=$(date +%s)
  crun kc135secant_run$N 0 $CAP d18_secant.py "$PY" -u $SWTM/d18_secant.py run $REC $ST $D $LO $HI $WSEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=cd134e2c,bc295fbc --ends=$WSEC/ends_run$N.jsonl >> $SEC/secant_run$N.log 2>&1
  rc=$RC; w=$(( $(date +%s) - s0 ))
  echo "exit $rc" >> $SEC/secant_run$N.log
  echo "kc135 secant run $N (bracket $LO, $HI): exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s (a stop)")" >> $SUM
  grep -E '^root:|^  lam' $SEC/secant_run$N.log | tail -n 12 | cut -c1-400 >> $SUM
  say "run $N exit $rc wall $w s capped $CAPPED"
  touch $SEC/run$N.done
done
