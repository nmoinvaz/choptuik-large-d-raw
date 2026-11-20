#!/bin/bash
{
# #1025 P4 share for another machine (p4_criteria.log): hybrid re-roots (float64 blocks 0-11, dd block 12) of delta-table records on
# their own states, by p4_hybrid.py. The cross-check row first: Fb, k_c 55, D 16 must give the Mac's hybrid root 2.244042809616683
# to 1e-5, or the batch stops before any other row. Then the rows in ROWS, one at a time.
# Extract with git show (LF line endings), not from a CRLF checkout.
#
# usage: p4_driver_w.sh WT RAW OUT
#   WT   a choptuik-large-d worktree at wip/ell1-highD 505d839940456a3d04321d75cf66cc3b5bc831c4 (dss_ell, ell_ddm, ddnp)
#   RAW  the root of a choptuik-large-d-raw clone holding every file in INPUTS below
#   OUT  this machine's raw task folder (it must exist with its README.md); writes OUT/p4_w.log, OUT/ell_p4_hybrid_1025_w.jsonl and
#        OUT/p4_rows/<D>_<kc>.log, and refuses if the log or jsonl exists
#   PY   environment variable: a python with numpy, scipy, mpmath and multidouble 5.1.0's package (dd_logdet)
#   THREADS  BLAS and rayon threads (default 4); ROW_TIMEOUT seconds per row (default 14400)
# Stop rules: the cross-check row must pass; the batch stops after 2 consecutive rows that time out or crash.
set -u
WT=$1; RAW=$2; OUT=$3; PY=${PY:-python3}; TH=${THREADS:-4}; ROW_TIMEOUT=${ROW_TIMEOUT:-14400}
WT_COMMIT=505d839940456a3d04321d75cf66cc3b5bc831c4
P4_BLOB=a402559b5d37661b49da50f07f877af21fd29b3a
MAC_ROOT=2.244042809616683
export OPENBLAS_NUM_THREADS=$TH OMP_NUM_THREADS=$TH MKL_NUM_THREADS=$TH VECLIB_MAXIMUM_THREADS=$TH RAYON_NUM_THREADS=$TH
export MSYS2_ARG_CONV_EXCL='*'                       # Git Bash: pass python's arguments as written
NICE=""; nice -n 10 true 2> /dev/null && NICE="nice -n 10"
wp() { if command -v cygpath > /dev/null; then cygpath -m "$1"; else echo "$1"; fi; }
LOG=$OUT/p4_w.log; JS=$OUT/ell_p4_hybrid_1025_w.jsonl
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $LOG; }
[ -f $OUT/README.md ] || { echo "refuse: $OUT/README.md missing"; exit 2; }
{ [ -e $LOG ] || [ -e $JS ]; } && { echo "refuse: $LOG or $JS exists (use a fresh folder)"; exit 2; }
[ "$(git -C $WT rev-parse HEAD)" = "$WT_COMMIT" ] || { echo "refuse: $WT is not at $WT_COMMIT"; exit 2; }
P4=$RAW/I1025-mac/p4_hybrid.py
[ "$(git hash-object $P4)" = "$P4_BLOB" ] || { echo "refuse: $P4 is not blob $P4_BLOB"; exit 2; }
INPUTS="
5be40af42cdcf2c1c3751c1b28a03884759fcbd4 I1025-mac/out/l1kc55Fb1025.jsonl
94c8b04878559d3ccdaef9535d4af6280d50edaf I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy
d9238215c3e1cfbcdeb1f990de24c41860c4c46a I1025-mac/out/sol_l1kc55Fb1025_D14.5000.npy
1679d5b7f5cd79e441ec33326076b842fdb74778 I1025-win2c/out/l1kc63Fz1025.jsonl
adc28f39b243d6c1da4cdba68380c02e687b5243 I1025-win2c/out/sol_l1kc63Fz1025_D15.5000.npy
10235f97e9b7c944579995ead4d527c38ce98f3a I1025-win2b/out/l1kc63Fu1025.jsonl
e122f7ea2009a8fdb17eb7a8c567067bd8175ed3 I1025-win2b/out/sol_l1kc63Fu1025_D16.2500.npy
"
bad=0
while read -r b p; do
  [ -z "$b" ] && continue
  [ -f $RAW/$p ] && [ "$(git hash-object $RAW/$p)" = "$b" ] || { echo "refuse: $RAW/$p missing or not blob $b"; bad=1; }
done <<< "$INPUTS"
[ $bad = 0 ] || exit 2
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { echo "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; exit 2; }
say "p4_driver_w.sh: inputs checked; WT $WT_COMMIT, p4_hybrid.py $P4_BLOB, PY $PY ($($PY -c 'import numpy, scipy, multidouble; print("numpy", numpy.__version__, "scipy", scipy.__version__, "multidouble", getattr(multidouble, "__version__", "?"))')), $TH threads, row timeout $ROW_TIMEOUT s"
export P4_WT_MATTER=$(wp $WT/solver/matter) P4_OUT=$(wp $JS)
mkdir -p $OUT/p4_rows
# ROWS: records state D (raw paths); the first is the cross-check row
ROWS="
I1025-mac/out/l1kc55Fb1025.jsonl I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy 16
I1025-win2c/out/l1kc63Fz1025.jsonl I1025-win2c/out/sol_l1kc63Fz1025_D15.5000.npy 15.5
I1025-mac/out/l1kc55Fb1025.jsonl I1025-mac/out/sol_l1kc55Fb1025_D14.5000.npy 14.5
I1025-win2b/out/l1kc63Fu1025.jsonl I1025-win2b/out/sol_l1kc63Fu1025_D16.2500.npy 16.25
"
fails=0; first=1; summary=""
while read -r rec st D; do
  [ -z "$rec" ] && continue
  say "row D $D: p4_hybrid.py $rec $st $D"
  timeout $ROW_TIMEOUT $NICE $PY -u $(wp $P4) $(wp $RAW/$rec) $(wp $RAW/$st) $D < /dev/null > $OUT/p4_rows/D$D.log 2>&1
  rc=$?
  grep -E '^D |^  lam' $OUT/p4_rows/D$D.log | tr -d '\r' >> $LOG
  line=$(tr -d '\r' < $OUT/p4_rows/D$D.log | grep -E "^D $D(\.0)? k_c [0-9]+ hybrid: lam" | tail -1)
  if [ $rc = 0 ] && [ -n "$line" ]; then
    v=$(tail -1 $JS | $PY -c 'import sys, json; r = json.loads(sys.stdin.read())
ok = r["record_system"] and r["n_signchanges_grid"] == 1 and r["n_changes_all"] == 1 and r["noise_robust"] and (r["bracket_width"] or 1) <= 1e-7
print(("PASS" if ok else "FAIL") + " lam " + repr(r["lam"]))' | tr -d '\r'); fails=0
  elif [ $rc = 124 ]; then v="TIMEOUT"; fails=$((fails + 1))
  else v="CRASH (exit $rc)"; fails=$((fails + 1)); fi
  say "row D $D: $v"
  summary="$summary
D $D: $v"
  if [ $first = 1 ]; then
    first=0
    lam=$(echo "$v" | awk '$1 == "PASS" {print $3}')
    [ -n "$lam" ] && $PY -c "import sys; sys.exit(0 if abs($lam - $MAC_ROOT) <= 1e-5 else 1)" \
      && say "cross-check PASS: $lam against the Mac's $MAC_ROOT ($($PY -c "print(f'{$lam - $MAC_ROOT:+.2e}')"))" \
      || { say "STOP: cross-check FAILED ($v against the Mac's $MAC_ROOT, bar 1e-5)"; break; }
  fi
  [ $fails -ge 2 ] && { say "STOP: two consecutive rows timed out or crashed"; break; }
done <<< "$ROWS"
say "summary:$summary"
say "p4_driver_w.sh done"
exit
}
