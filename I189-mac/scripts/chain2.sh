#!/usr/bin/env bash
# the second process of the #189 runs: the 6b1 mutations, then the kmin check, then the 6a mutations
set -u
D=$(cd "$(dirname "$0")" && pwd)
W=${W:-/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a2e622b9920aedaa1/solver/proof/review_189}
R=$(dirname "$D")
"$D/mut_b1.sh"
cd "$W" && "$W/run.sh" "$R/kmin_check.log" /Users/nathan/venv-qd/bin/python -u kmin_check.py
"$D/mut_a.sh"
