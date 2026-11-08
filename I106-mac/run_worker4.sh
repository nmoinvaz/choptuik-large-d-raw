#!/bin/bash
# Issue #106, outside the criteria: 40x77 and 40x81 at more D on the path (25.08, 29.98, 34.99, 44.96, 50.01, 54.996),
# each from the path's 40x79 root there. On 40x75..83 at D 20, 40 and 60, Delta - Delta_hp alternates in sign with
# N (step 2) and falls geometrically, so the size of 40x79's truncation is better read from its neighbours than from its
# own value, which crosses zero near D = 46.5.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
cd "$CODE" || exit 2
job() {   # job TAG NEWTON_TOL START GRID
  local out="$HERE/res" tag="$1" nt="$2" st="$3" gr="$4"
  if [ -e "$out/done_$tag" ]; then echo "== skip $tag (done)"; return; fi
  if [ ! -e "$st" ]; then echo "== skip $tag (no start $st)"; return; fi
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC start $tag: $gr from $st"
  nice -n 10 $PY solver/rt/rt_run.py --start "$st" --grids "$gr" $OPTS --newton_tol "$nt" --tol 1e-4 \
      --out "$out" --tag "$tag"
  local rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $tag"
  touch "$out/done_$tag"
}
for D in D50.0075 D44.9634 D34.9933 D29.9847 D25.0797 D54.9961; do
  NT=1e-40; [ $D = D54.9961 ] && NT=1e-36
  for G in 40x77 40x81; do
    job P_${G}_$D $NT "$HERE/cont/cont_40x79_${D}_40x79.npz" $G
  done
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
