#!/usr/bin/env bash
# lemma 6a(5) mutations on the backward flow xi = 0.3 -> 0.067: each must make the review's check (capd_m5 c1 against
# I103's X and B, compare.py --expect=miss) and the original (lemma6_jump_M.backward under the same mutation, its X and
# B against I103's) fail; the two mutated runs must still agree with each other. Run under nice -n 10.
set -u
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I189-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
BOX="$RAW/I103-macm3/A_M2_6a_M5_sub1e-18.json"
B103="$RAW/I103-macm3/B_M5_sub1e-18.json"
ONLY=${ONLY:-"sign eps start"}
cd "$W" || exit 2
export CAPD_M5_PROGRESS=50
for m in $ONLY; do
  case $m in
    sign) CA=(--sign=-1); OM=sign; ST="$R/inputs/start6a_I103.txt" ;;
    eps) CA=(--eps=1e-5); OM=eps=1e-5; ST="$R/inputs/start6a_I103.txt" ;;
    start) CA=(); OM=start=6:1e-7; ST="$R/inputs/start6a_I103_perturb6_1e-7.txt" ;;
  esac
  "$W/run.sh" "$R/mut_a_capd_$m.log" "$W/build/capd_m5" c1 "$ST" "$R/inputs/path6a.txt" --order=20 --tol=1e-17 \
    "${CA[@]}"
  "$W/run.sh" "$R/cmp_mut_a_capd_$m.log" "$PY" compare.py a "$R/mut_a_capd_$m.log" "$B103" --expect=miss \
    --json="$R/cmp_mut_a_capd_$m.json"
  "$W/run.sh" "$R/mut_a_orig_$m.log" "$PY" -u orig_mut.py a "$BOX" --wf=0.999228404 --h=1e-18 --mutate=$OM \
    --save-B="$R/B_orig_mut_$m.json"
  "$W/run.sh" "$R/cmp_mut_a_orig_$m.log" "$PY" compare.py BB "$R/B_orig_mut_$m.json" "$B103" --expect=miss \
    --json="$R/cmp_mut_a_orig_$m.json"
  "$W/run.sh" "$R/cmp_mut_a_cross_$m.log" "$PY" compare.py a "$R/mut_a_capd_$m.log" "$R/B_orig_mut_$m.json" \
    --expect=overlap --json="$R/cmp_mut_a_cross_$m.json"
done
