#!/usr/bin/env bash
# b1_row.sh J[:sign]: lemma 6b1(5) row J (#208). capd_m5 c0 (128-bit C^0 doubleton, order 32, tol 1e-26, as #189 ran
# rows 0 and 9) from the stored C^1 start at s0 = 405 e^{-3 i pi/4} along ray legs 1..J and row J's arc, then
# compare.py b1 against ray.json starts and I39-mac/disc_inputs/row_JJ.json, then ray_identity.sh against #189's
# b1_clean.log. J:sign is the mutation (--sign=-1 flips [[C E] P] in V'), which must miss (--expect=miss) and must
# differ from #189's ray boxes. Run under nice -n 10.
set -u
J=${1%%:*}
MUT=none
case $1 in *:*) MUT=${1#*:} ;; esac
jj=$(printf %02d "$J")
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a1cd434a46c3bedb1/solver/proof/review_189}
R=${R:-/Users/nathan/Source/choptuik-large-d-raw/I208-mac}
RAW=$(dirname "$R")
PY=${PY:-/Users/nathan/venv-qd/bin/python}
RAY="$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json"
export CAPD_M5_PROGRESS=10
case $MUT in
  none) name=b1_row$jj; CA=(); EX=overlap; ID=same ;;
  sign) name=mut_sign_row$jj; CA=(--sign=-1); EX=miss; ID=differ ;;
  *) echo "unknown mutation $MUT"; exit 2 ;;
esac
"$W/run.sh" "$R/$name.log" "$W/build/capd_m5" c0 "$R/inputs/start6b1.txt" "$R/inputs/path6b1_row$jj.txt" --prec=128 \
  --order=32 --tol=1e-26 ${CA[@]+"${CA[@]}"}
cd "$W" || exit 2
"$W/run.sh" "$R/cmp_$name.log" "$PY" compare.py b1 "$R/$name.log" "$RAY" "$RAW/I39-mac/disc_inputs/row_$jj.json" \
  --expect=$EX --json="$R/cmp_$name.json"
if [ "$J" -gt 0 ]; then
  "$W/run.sh" "$R/rayid_$name.log" "$R/scripts/ray_identity.sh" "$R/$name.log" "$RAW/I189-mac/b1_clean.log" "$J" "$ID"
fi
