#!/bin/bash
# #1025 winb, k_c 143 lane: the source checks by hand, before the README (read-only; the same five runs as the regrid driver's step 3): the k_c 135 check accepts win2's k_c 135 D 23.0 state (exit 0),
# its --mutate=F and --mutate=steps exit 1 each, the k_c 127 and k_c 143 checks refuse it (exit 1 each). Output: prep_source_checks_by_hand.txt next to this script.
S=/c/Users/nathan/Source/kc143d23_1025
PY=/c/Users/nathan/Source/venv-md510/Scripts/python.exe
WTM=/c/Users/nathan/Source/choptuik-i1025k79/solver/matter
REC=$S/inputs/l1kc135win2d23.jsonl
ST=$S/inputs/sol_l1kc135win2d23_D23.0000.npy
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONDONTWRITEBYTECODE=1
OUT=$S/prep_source_checks_by_hand.txt
: > "$OUT"
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC start" >> "$OUT"
run() {
  local label=$1; shift
  local t0=$(date +%s)
  "$PY" "$@" > "$S/prep_tmp.txt" 2>&1; local rc=$?
  { echo "== $label: exit $rc ($(( $(date +%s) - t0 )) s)"; tail -3 "$S/prep_tmp.txt"; } >> "$OUT"
}
run "kc135 selftest (0 wanted)" $S/inputs/kc135_syscheck_1025.py --selftest
run "kc135 check on the source (0 wanted)" $S/inputs/kc135_syscheck_1025.py $REC $ST 23.0 $WTM
run "kc135 --mutate=F (1 wanted)" $S/inputs/kc135_syscheck_1025.py $REC $ST 23.0 $WTM --mutate=F
run "kc135 --mutate=steps (1 wanted)" $S/inputs/kc135_syscheck_1025.py $REC $ST 23.0 $WTM --mutate=steps
run "kc127 check on the source (1 wanted: refuses)" $S/inputs/kc127_syscheck_1025.py $REC $ST 23.0 $WTM
run "kc143 check on the source (1 wanted: refuses)" $S/inputs/kc143_syscheck_1025.py $REC $ST 23.0 $WTM
echo "# $(date -u '+%Y-%m-%d %H:%M:%S') UTC end" >> "$OUT"
mv "$S/prep_tmp.txt" /c/Users/nathan/Source/_trash_1025/kc143_prep_tmp.txt
