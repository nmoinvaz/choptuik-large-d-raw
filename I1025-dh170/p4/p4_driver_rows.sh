#!/bin/bash
{
# #1025 P4 share for another machine (p4_criteria.log): hybrid re-roots (float64 blocks 0-11, dd block 12) of delta-table records on
# their own states, by p4_hybrid.py, for the rows of a row list. p4_driver_w.sh with the rows read from a pinned file and the inputs
# hashed with git hash-object --no-filters. The cross-check row runs first: Fb, k_c 55, D 16 must give the Mac's hybrid root
# 2.244042809616683 to 1e-5, or the batch stops before any listed row. Extract with git show (LF line endings), not from a CRLF checkout.
#
# usage: p4_driver_rows.sh WT RAW OUT ROWLIST ROWLIST_BLOB
#   WT       a choptuik-large-d worktree at wip/ell1-highD 505d839940456a3d04321d75cf66cc3b5bc831c4 (dss_ell, ell_ddm, ddnp)
#   RAW      the root of a choptuik-large-d-raw clone holding p4_hybrid.py and every input the cross-check row and ROWLIST name
#   OUT      this machine's raw task folder or a subfolder (it must hold a README.md); writes OUT/p4_w.log,
#            OUT/ell_p4_hybrid_1025_w.jsonl and OUT/p4_rows/row<i>_D<D>.log, and refuses if the log or jsonl exists
#   ROWLIST  a file of rows "RECORDS RECORDS_BLOB STATE STATE_BLOB D TIMEOUT_S" (raw paths; # lines and blank lines skipped)
#   ROWLIST_BLOB  its blob id (git hash-object --no-filters); the batch refuses another file
#   PY       environment variable: a python with numpy, scipy, mpmath and multidouble 5.1.0's package (dd_logdet)
#   THREADS  BLAS and rayon threads (default 4); CROSS_TIMEOUT seconds for the cross-check row (default 14400)
# Stop rules: the cross-check row must pass; each row has its own timeout; the batch stops after 2 consecutive rows that time out
# or crash.
set -u
[ $# = 5 ] || { echo "usage: p4_driver_rows.sh WT RAW OUT ROWLIST ROWLIST_BLOB"; exit 2; }
WT=$1; RAW=$2; OUT=$3; ROWLIST=$4; ROWLIST_BLOB=$5; PY=${PY:-python3}; TH=${THREADS:-4}; CROSS_TIMEOUT=${CROSS_TIMEOUT:-14400}
WT_COMMIT=505d839940456a3d04321d75cf66cc3b5bc831c4
P4_BLOB=a402559b5d37661b49da50f07f877af21fd29b3a
MAC_ROOT=2.244042809616683
CROSS="I1025-mac/out/l1kc55Fb1025.jsonl 5be40af42cdcf2c1c3751c1b28a03884759fcbd4 I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy 94c8b04878559d3ccdaef9535d4af6280d50edaf 16 $CROSS_TIMEOUT"
export OPENBLAS_NUM_THREADS=$TH OMP_NUM_THREADS=$TH MKL_NUM_THREADS=$TH VECLIB_MAXIMUM_THREADS=$TH RAYON_NUM_THREADS=$TH
export MSYS2_ARG_CONV_EXCL='*'                       # Git Bash: pass python's arguments as written
NICE=""; nice -n 10 true 2> /dev/null && NICE="nice -n 10"
wp() { if command -v cygpath > /dev/null; then cygpath -m "$1"; else echo "$1"; fi; }
hb() { git hash-object --no-filters "$1"; }          # the bytes as stored, on every platform
LOG=$OUT/p4_w.log; JS=$OUT/ell_p4_hybrid_1025_w.jsonl
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $LOG; }
[ -f $OUT/README.md ] || { echo "refuse: $OUT/README.md missing"; exit 2; }
{ [ -e $LOG ] || [ -e $JS ]; } && { echo "refuse: $LOG or $JS exists (use a fresh folder)"; exit 2; }
[ "$(git -C $WT rev-parse HEAD)" = "$WT_COMMIT" ] || { echo "refuse: $WT is not at $WT_COMMIT"; exit 2; }
P4=$RAW/I1025-mac/p4_hybrid.py
[ "$(hb $P4)" = "$P4_BLOB" ] || { echo "refuse: $P4 is not blob $P4_BLOB"; exit 2; }
[ -f "$ROWLIST" ] && [ "$(hb "$ROWLIST")" = "$ROWLIST_BLOB" ] || { echo "refuse: $ROWLIST missing or not blob $ROWLIST_BLOB"; exit 2; }
ROWS="$CROSS
$(tr -d '\r' < "$ROWLIST" | grep -vE '^[[:space:]]*(#|$)')"
bad=0; n=0
while read -r rec rb st sb D to; do
  n=$((n + 1))
  [ -n "$to" ] && [ "$to" -gt 0 ] 2> /dev/null || { echo "refuse: row $n has no timeout: $rec $st $D"; bad=1; }
  for pb in "$rec $rb" "$st $sb"; do
    set -- $pb
    [ -f $RAW/$1 ] && [ "$(hb $RAW/$1)" = "$2" ] || { echo "refuse: $RAW/$1 missing or not blob $2"; bad=1; }
  done
done <<< "$ROWS"
[ $bad = 0 ] || exit 2
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { echo "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; exit 2; }
say "p4_driver_rows.sh: inputs checked ($n rows, the cross-check first; row list $ROWLIST_BLOB); WT $WT_COMMIT, p4_hybrid.py $P4_BLOB, PY $PY ($($PY -c 'import numpy, scipy; print("numpy", numpy.__version__, "scipy", scipy.__version__)' | tr -d '\r')), $TH threads"
export P4_WT_MATTER=$(wp $WT/solver/matter) P4_OUT=$(wp $JS)
mkdir -p $OUT/p4_rows
fails=0; i=0; summary=""
while read -r rec rb st sb D to; do
  i=$((i + 1)); RL=$OUT/p4_rows/row${i}_D$D.log
  say "row $i D $D: p4_hybrid.py $rec $st $D (timeout $to s)"
  timeout $to $NICE $PY -u $(wp $P4) $(wp $RAW/$rec) $(wp $RAW/$st) $D < /dev/null > $RL 2>&1
  rc=$?
  grep -E '^D |^  lam' $RL | tr -d '\r' >> $LOG
  line=$(tr -d '\r' < $RL | grep -E "^D $D(\.0)? k_c [0-9]+ hybrid: lam" | tail -1)
  if [ $rc = 0 ] && [ -n "$line" ]; then
    v=$(tail -1 $JS | tr -d '\r' | $PY -c 'import sys, json; r = json.loads(sys.stdin.read()); D = float(sys.argv[1])
ok = r["D"] == D and r["record_system"] and r["n_signchanges_grid"] == 1 and r["n_changes_all"] == 1 and r["noise_robust"] and (r["bracket_width"] or 1) <= 1e-7
print(("PASS" if ok else "FAIL") + " lam " + repr(r["lam"]) + " k_c " + str(r["kc"]))' $D | tr -d '\r'); fails=0
  elif [ $rc = 124 ]; then v="TIMEOUT"; fails=$((fails + 1))
  else v="CRASH (exit $rc)"; fails=$((fails + 1)); fi
  say "row $i D $D: $v"
  summary="$summary
row $i D $D: $v"
  if [ $i = 1 ]; then
    lam=$(echo "$v" | awk '$1 == "PASS" {print $3}')
    [ -n "$lam" ] && $PY -c "import sys; sys.exit(0 if abs($lam - $MAC_ROOT) <= 1e-5 else 1)" \
      && say "cross-check PASS: $lam against the Mac's $MAC_ROOT ($($PY -c "print(f'{$lam - $MAC_ROOT:+.2e}')" | tr -d '\r'))" \
      || { say "STOP: cross-check FAILED ($v against the Mac's $MAC_ROOT, bar 1e-5)"; break; }
  fi
  [ $fails -ge 2 ] && { say "STOP: two consecutive rows timed out or crashed"; break; }
done <<< "$ROWS"
say "summary:$summary"
say "p4_driver_rows.sh done"
exit
}
