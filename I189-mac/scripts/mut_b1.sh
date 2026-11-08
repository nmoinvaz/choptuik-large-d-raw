#!/usr/bin/env bash
# lemma 6b1(5) mutations on the first ray leg (|u| = 405 -> 378.36): each must make the review's check (capd_m5 against
# the stored ray box, compare.py --expect=miss) and the original (validated_int.Lohner under the same mutation against
# the stored box) fail; the two mutated runs must still agree with each other (compare.py logs). Plus the original
# unmutated as the control (must overlap the stored box). Run under nice -n 10.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I189-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
RAY="$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json"
ROW="$RAW/I39-mac/disc_inputs/row_17.json"
cd "$W" || exit 2
# the original, unmutated (control)
"$W/run.sh" "$R/mut_b1_orig_none.log" "$PY" -u orig_mut.py b1 "$RAY" --legs=1 --mutate=none
"$W/run.sh" "$R/cmp_mut_b1_orig_none.log" "$PY" compare.py b1 "$R/mut_b1_orig_none.log" "$RAY" "$ROW" --expect=overlap \
  --json="$R/cmp_mut_b1_orig_none.json"
for m in sign eps start; do
  case $m in
    sign) CA=(--sign=-1); OM=sign; ST="$R/inputs/start6b1.txt" ;;
    eps) CA=(--eps=1e-9); OM=eps=1e-9; ST="$R/inputs/start6b1.txt" ;;
    start) CA=(); OM=start=6:1e-15; ST="$R/inputs/start6b1_perturb6_1e-15.txt" ;;
  esac
  "$W/run.sh" "$R/mut_b1_capd_$m.log" "$W/build/capd_m5" c0 "$ST" "$R/inputs/path_leg1.txt" --prec=128 --order=32 \
    --tol=1e-26 "${CA[@]}"
  "$W/run.sh" "$R/cmp_mut_b1_capd_$m.log" "$PY" compare.py b1 "$R/mut_b1_capd_$m.log" "$RAY" "$ROW" --expect=miss \
    --json="$R/cmp_mut_b1_capd_$m.json"
  "$W/run.sh" "$R/mut_b1_orig_$m.log" "$PY" -u orig_mut.py b1 "$RAY" --legs=1 --mutate=$OM
  "$W/run.sh" "$R/cmp_mut_b1_orig_$m.log" "$PY" compare.py b1 "$R/mut_b1_orig_$m.log" "$RAY" "$ROW" --expect=miss \
    --json="$R/cmp_mut_b1_orig_$m.json"
  "$W/run.sh" "$R/cmp_mut_b1_cross_$m.log" "$PY" compare.py logs "$R/mut_b1_capd_$m.log" "$R/mut_b1_orig_$m.log" \
    --expect=overlap --json="$R/cmp_mut_b1_cross_$m.json"
done
