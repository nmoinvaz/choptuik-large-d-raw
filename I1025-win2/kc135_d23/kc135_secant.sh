#!/bin/bash
# #1025 kc135_d23 on win2 (the coordinator's hc of 2026-11-26 14:14 UTC), step 5: the secant, d18_secant.py run (92b9bf53, blob eb1396ad) on the scan's one robust bracket (0.045, 0.050), --tol=1e-5 --maxev=10,
# one process of one thread (Normal), cap 43200 s on the exact root pid (crun); --pin of the accepted state and record; --ends: the two ends' records are taken from this scan's own rows at lambda 0.045 and 0.050 (the
# same state and tool: saves two evaluations of 2.4 h each; their robustness is then the 1e-15 noise test's, which the scan's records carry as noise_robust).
# usage: kc135_secant.sh LO HI   (e.g. 0.045 0.05)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc135_d23; WOUT=D:/choptuik-i935-raw/I1025-win2/kc135_d23
SEC=$OUT/secant; WSEC=$WOUT/secant; SUM=$SEC/summary_secant.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
SWT=/d/choptuik-i1025secant92; SWTM=D:/choptuik-i1025secant92/solver/matter
NEW=l1kc135win2d23; D=23.0; CAP=43200
LO=${1:-0.045}; HI=${2:-0.05}
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$SWTM PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
mkdir -p $SEC
refuse() { log "kc135 secant STOP: $*"; echo "kc135 secant STOP: $*" >> $SUM; exit ${2:-1}; }
h=$(git hash-object --no-filters $SWT/solver/matter/d18_secant.py); case "$h" in eb1396ad*) ;; *) refuse "d18_secant.py is blob $h, not eb1396ad";; esac
[ "$(git -C $SWT rev-parse HEAD | cut -c1-8)" = 92b9bf53 ] || refuse "the worktree is not at 92b9bf53"
[ "$(git hash-object --no-filters $OUT/sol_${NEW}_D23.0000.npy | cut -c1-8)" = cd134e2c ] || refuse "the state is not blob cd134e2c"
[ "$(git hash-object --no-filters $OUT/${NEW}.jsonl | cut -c1-8)" = bc295fbc ] || refuse "the record is not blob bc295fbc"
# the two ends' rows from the scan files (the rows at LO and HI)
"$PY" -I -c "
import json, glob
rows = []
for f in sorted(glob.glob('$WOUT/scan/scan_D23.0_p*.jsonl')):
    rows += [json.loads(l) for l in open(f) if l.strip()]
ends = [r for r in rows if abs(r['lam'] - $LO) < 1e-12 or abs(r['lam'] - $HI) < 1e-12]
assert len({round(r['lam'], 6) for r in ends}) == 2, 'both ends are needed in the scan files'
seen = {}
for r in ends:
    seen.setdefault(round(r['lam'], 6), r)
open('$WSEC/ends_${LO}_${HI}.jsonl', 'w').write(''.join(json.dumps(r) + chr(10) for r in seen.values()))
print('ends file: lambdas', sorted(seen))" || refuse "the ends file could not be made"
REC=$WOUT/${NEW}.jsonl; ST=$WOUT/sol_${NEW}_D23.0000.npy
cd $SWT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $PY -u $SWTM/d18_secant.py run $REC $ST $D $LO $HI $WSEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=cd134e2c,bc295fbc --ends=$WSEC/ends_${LO}_${HI}.jsonl (cwd $SWTM, 1 thread, Normal)"; } > $SEC/secant.log
s0=$(date +%s)
crun kc135secant 0 $CAP d18_secant.py "$PY" -u $SWTM/d18_secant.py run $REC $ST $D $LO $HI $WSEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=cd134e2c,bc295fbc --ends=$WSEC/ends_${LO}_${HI}.jsonl >> $SEC/secant.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $SEC/secant.log
echo "kc135 secant (bracket $LO, $HI): exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", CAPPED at $CAP s (a stop)")" >> $SUM
grep -E '^root:|^  lam' $SEC/secant.log | tail -n 12 | cut -c1-400 >> $SUM
log "kc135 secant exit $rc wall $w s capped $CAPPED"
touch $SEC/secant.done
exit 0
