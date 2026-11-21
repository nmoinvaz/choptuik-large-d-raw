#!/bin/bash
{
# #1025 winb follow-on (coordinator's order, 2026-11-21): hybrid roots past D 17 on winb's own k_c 63 states, one row at a time, by raw
# I1025-mac/p4_hybrid.py (blob a402559b), after the P4 driver (p4_driver_w.sh) has ended. Row A: D 17.5, row B: D 17.75. Each row:
# p4_hybrid.py on a stub record (the guess and window written into the README before the run), then raw I1025-mac/signtest.py at the hybrid
# lambda -/+ 0.02, then verdict_p4hi_1025.py (P4 rules, edge rule, signtest). A thin driver: no solver code.
#
# usage: p4hi_driver_1025.sh WT RAW OUT WAITLOG
#   WT       choptuik-large-d worktree at 505d839940456a3d04321d75cf66cc3b5bc831c4 (the P4 rows' worktree)
#   RAW      folder of git-show files from raw origin/main (prep_p4hi_inputs_1025.sh)
#   OUT      staging folder holding README.md and the two stub records; writes OUT/p4hi_w.log, OUT/ell_p4_hybrid_1025_w_highD.jsonl, OUT/rows/
#   WAITLOG  P4's p4_w.log: the rows start when it holds "p4_driver_w.sh done"
#   PY       environment variable: python with numpy, scipy, mpmath, multidouble 5.1.0 (dd_logdet); THREADS (default 4); ROW_TIMEOUT (default 21600 s)
# No nice: the launcher starts this at BelowNormal and the children inherit it.
set -u
WT=$1; RAW=$2; OUT=$3; WAITLOG=$4; PY=${PY:-python3}; TH=${THREADS:-4}; ROW_TIMEOUT=${ROW_TIMEOUT:-21600}
WT_COMMIT=505d839940456a3d04321d75cf66cc3b5bc831c4
export OPENBLAS_NUM_THREADS=$TH OMP_NUM_THREADS=$TH MKL_NUM_THREADS=$TH VECLIB_MAXIMUM_THREADS=$TH RAYON_NUM_THREADS=$TH
export MSYS2_ARG_CONV_EXCL='*'
wp() { if command -v cygpath > /dev/null; then cygpath -m "$1"; else echo "$1"; fi; }
HERE=$(cd "$(dirname "$0")" && pwd)
LOG=$OUT/p4hi_w.log; JS=$OUT/ell_p4_hybrid_1025_w_highD.jsonl
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $LOG; }
[ -f $OUT/README.md ] || { echo "refuse: $OUT/README.md missing"; exit 2; }
{ [ -e $LOG ] || [ -e $JS ]; } && { echo "refuse: $LOG or $JS exists (use a fresh folder)"; exit 2; }
[ "$(git -C $WT rev-parse HEAD)" = "$WT_COMMIT" ] || { echo "refuse: $WT is not at $WT_COMMIT"; exit 2; }
P4=$RAW/I1025-mac/p4_hybrid.py; ST=$RAW/I1025-mac/signtest.py; VD=$HERE/verdict_p4hi_1025.py
[ "$(git hash-object --no-filters $P4)" = a402559b5d37661b49da50f07f877af21fd29b3a ] || { echo "refuse: $P4 is not blob a402559b"; exit 2; }
[ "$(git hash-object --no-filters $ST)" = 179ea09681b0a75f7cefdff98984b48051b3f085 ] || { echo "refuse: $ST is not blob 179ea096"; exit 2; }
[ -f $VD ] || { echo "refuse: $VD missing"; exit 2; }
# row name, D, state (under RAW), stub record (under OUT), pinned state blob, reference value for the report ("-" for none)
ROWS="
A 17.5 I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy stub_rowA_l1kc63Fw1025_D17.5_trendguess.jsonl d85f7b71c2c1750ca91d941320b9f2cdf57fe029 1.9522
B 17.75 I1025-win/out/sol_l1kc63W1025_D17.750000.npy stub_rowB_l1kc63W1025_D17.75_leapline.jsonl de9fc3e55aa46bafd4ef62536861f94aed9e3035 -
"
bad=0
while read -r n D st stub blob ref; do
  [ -z "$n" ] && continue
  [ -f $OUT/$stub ] || { echo "refuse: $OUT/$stub missing"; bad=1; }
  [ "$(git hash-object --no-filters $RAW/$st)" = "$blob" ] || { echo "refuse: $RAW/$st is not blob $blob"; bad=1; }
done <<< "$ROWS"
[ $bad = 0 ] || exit 2
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { echo "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; exit 2; }
export P4_WT_MATTER=$(wp $WT/solver/matter) P4_OUT=$(wp $JS)
mkdir -p $OUT/rows
say "p4hi_driver_1025.sh: inputs checked; WT $WT_COMMIT, p4_hybrid.py a402559b, signtest.py 179ea096, PY $PY, $TH threads, row timeout $ROW_TIMEOUT s; waiting for '$WAITLOG' to hold 'p4_driver_w.sh done'"
until grep -q 'p4_driver_w.sh done' "$WAITLOG" 2> /dev/null; do sleep 30; done
say "P4 driver done; rows start"
summary=""
while read -r n D st stub blob ref; do
  [ -z "$n" ] && continue
  say "row $n D $D: p4_hybrid.py $stub $st $D"
  timeout $ROW_TIMEOUT $PY -u $(wp $P4) $(wp $OUT/$stub) $(wp $RAW/$st) $D < /dev/null > $OUT/rows/D$D.log 2>&1
  rc=$?
  grep -E '^D |^  lam' $OUT/rows/D$D.log | tr -d '\r' >> $LOG
  line=$(tr -d '\r' < $OUT/rows/D$D.log | grep -E "^D $D(\.0)? k_c [0-9]+ hybrid: lam" | tail -1)
  v=""
  if [ $rc = 0 ] && [ -n "$line" ] && ! echo "$line" | grep -q 'lam None'; then
    say "row $n D $D: hybrid done; signtest at lam -/+ 0.02"
    (cd $WT/solver/matter && timeout 7200 $PY -u $(wp $ST) $(wp $RAW/$st) $D 63 around=$(wp $JS):$D:0.02 < /dev/null > $OUT/rows/signtest_D$D.log 2>&1)
    say "row $n D $D: signtest exit $?"
    RA=""; [ "$ref" != "-" ] && RA="--ref $ref"
    $PY $(wp $VD) $(wp $JS) $D $(wp $OUT/rows/signtest_D$D.log) $RA < /dev/null 2>&1 | tr -d '\r' | tee $OUT/rows/verdict_D$D.log >> $LOG
    v=$(grep -E '^VERDICT' $OUT/rows/verdict_D$D.log | tail -1)
    [ -n "$v" ] || v="VERDICT script gave no verdict"
  elif [ $rc = 124 ]; then v="TIMEOUT after $ROW_TIMEOUT s"
  else v="CRASH or no root (exit $rc): $line"; fi
  say "row $n D $D: $v"
  summary="$summary
row $n D $D: $v"
done <<< "$ROWS"
say "summary:$summary"
say "p4hi_driver_1025.sh done"
exit
}
