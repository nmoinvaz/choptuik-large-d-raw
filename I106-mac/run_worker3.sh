#!/bin/bash
# Issue #106, outside the criteria: after run_worker2.sh, the next grids out in N, 40x75 and 40x83, at D 20.04, 40.02
# and 60.00 from the B roots. On 40x77, 79 and 81 the sign of Delta - Delta_hp alternates with N (79 against 77 and
# 81), so these show whether that is a pattern in N mod 4 and how the size falls with N.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
cd "$CODE" || exit 2
until grep -q "queue done" "$HERE/worker2.stdout" 2>/dev/null; do sleep 30; done
job() {   # job TAG NEWTON_TOL START GRID
  local out="$HERE/res" tag="$1" nt="$2" st="$3" gr="$4"
  if [ -e "$out/done_$tag" ]; then echo "== skip $tag (done)"; return; fi
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC start $tag: $gr from $st"
  nice -n 10 $PY solver/rt/rt_run.py --start "$st" --grids "$gr" $OPTS --newton_tol "$nt" --tol 1e-4 \
      --out "$out" --tag "$tag"
  local rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $tag"
  touch "$out/done_$tag"
}
for D in D60.0020 D40.0201 D20.0437; do
  NT=1e-40; [ $D = D60.0020 ] && NT=1e-36
  for G in 40x75 40x83; do
    job N_${G}_$D $NT "$HERE/res/B_40x79_${D}_${D}_40x79.npz" $G
  done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
