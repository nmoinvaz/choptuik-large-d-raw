#!/usr/bin/env bash
# the second process after chain2.sh: lemma 6a(5) at p^ against I184-macm3's B, then the series check of the start data,
# then chain1c.sh
set -u
D=$(cd "$(dirname "$0")" && pwd)
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=$(dirname "$D")
RAW=$(dirname "$R")
TAG=I184 START="$R/inputs/start6a_I184_phat.txt" B="$RAW/I184-macm3/B_M5_sub1e-18_phat.json" "$D/a_clean.sh"
cd "$W" && "$W/run.sh" "$R/series_check.log" /Users/nathan/venv-qd/bin/python -u series_check.py \
  "$RAW/I38-macm3/lemma6b1_runs_M5_cert/ray.json"
"$D/chain1c.sh"
