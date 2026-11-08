#!/bin/bash
# Issue #106: the queue of re-solves for the second process (second starts B, controls, the coefficient mutation,
# neighbouring grids, N_t). Each job writes OUT/TAG.{log,jsonl}, its state and a done marker OUT/done_TAG; a restart
# skips the jobs marked done.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW="$(cd "$HERE/.." && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
I105=$RAW/I105-mac/cont; I145=$RAW/I145-mac
cd "$CODE" || exit 2

job() {   # job OUTDIR TAG NEWTON_TOL TOL START GRID [extra rt_run.py args]
  local out="$HERE/$1" tag="$2" nt="$3" tol="$4" st="$5" gr="$6"; shift 6
  mkdir -p "$out"
  if [ -e "$out/done_$tag" ]; then echo "== skip $tag (done)"; return; fi
  if [ ! -e "$st" ]; then echo "== skip $tag (no start $st)"; return; fi
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC start $tag: $gr from $st"
  nice -n 10 $PY solver/rt/rt_run.py --start "$st" --grids "$gr" $OPTS --newton_tol "$nt" --tol "$tol" \
      --out "$out" --tag "$tag" "$@"
  local rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $tag"
  touch "$out/done_$tag"
}

# second starts B on 40x79 (D 60 first: the hardest case, the pilot)
job res B_40x79_D60.0020 1e-36 1e-4 "$I145/cont/cont_32x101_D60.0020_32x101.npz" 40x79
job res B_40x79_D40.0201 1e-40 1e-4 "$I145/cont/cont_32x101_D40.0201_32x101.npz" 40x79
job res B_40x79_D20.0437 1e-40 1e-4 "$I105/cont_32x101_D20.0437_32x101.npz" 40x79
# controls: within 1e-9 of hp
job controls C_32x121_D20.0437 1e-40 1e-9 "$I105/cont_32x101_D20.0437_32x101.npz" 32x121
job controls C_32x121_D40.0201 1e-40 1e-9 "$I145/cont/cont_32x101_D40.0201_32x101.npz" 32x121
job controls C_32x101_D60.0020 1e-36 1e-9 "$I145/fol/fol_32x121_D60.0020_32x121.npz" 32x101
# the coefficient mutation on 40x79 at D 20.04 from root A (must exit 1)
job controls coef_40x79_D20.0437 1e-40 1e-4 "$HERE/cont/cont_40x79_D20.0437_40x79.npz" 40x79 --mutate=coef
# neighbouring grids in N, from the B roots
for D in D20.0437 D40.0201 D60.0020; do
  NT=1e-40; [ $D = D60.0020 ] && NT=1e-36
  for G in 40x77 40x81; do
    job res N_${G}_$D $NT 1e-4 "$HERE/res/B_40x79_${D}_${D}_40x79.npz" $G
  done
done
# the t resolution: 32x79 at D 40.02 and 60.00 from the B roots
job res Nt_32x79_D40.0201 1e-40 1e-4 "$HERE/res/B_40x79_D40.0201_D40.0201_40x79.npz" 32x79
job res Nt_32x79_D60.0020 1e-36 1e-4 "$HERE/res/B_40x79_D60.0020_D60.0020_40x79.npz" 32x79
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
