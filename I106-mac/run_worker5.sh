#!/bin/bash
# Issue #106, outside the criteria: 40x77 and 40x81 at D = 70, 80, 90 and 100, each from the extension's 40x79 root
# there (run_ext.sh), as the neighbours of 40x79 past D = 60, and at D 80 and 100 the second starts for 40x79 (the 40x81
# and 40x77 roots resampled back to 40x79). Each D waits for its state. One process at a time.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol 1e-36"
cd "$CODE" || exit 2
for D in 70 80 90 100; do
  # run_ext.sh's rounds name the states ext_40x79_* and rename them cont_40x79_* when a round ends
  sx=$(printf "%s/cont/ext_40x79_D%.4f_40x79.npz" "$HERE" "$D")
  sc=$(printf "%s/cont/cont_40x79_D%.4f_40x79.npz" "$HERE" "$D")
  st=""
  while [ -z "$st" ]; do
    for f in "$sx" "$sc"; do
      if [ -e "$f" ] && [ $(( $(date +%s) - $(stat -f %m "$f") )) -ge 20 ]; then st="$f"; break; fi
    done
    [ -n "$st" ] && break
    pgrep -f "run_ext.sh" > /dev/null || { echo "== run_ext.sh ended before D $D"; break 2; }
    sleep 30
  done
  cp "$st" "$HERE/res/start_40x79_D$D.npz"      # a copy: the rename at the end of a round cannot move it
  st="$HERE/res/start_40x79_D$D.npz"
  for G in 40x77 40x81; do
    tag=Q_${G}_D$D
    [ -e "$HERE/res/done_$tag" ] && { echo "== skip $tag (done)"; continue; }
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC start $tag: $G from $st"
    nice -n 10 $PY solver/rt/rt_run.py --start "$st" --grids "$G" $OPTS --tol 1e-3 --out "$HERE/res" --tag "$tag"
    rc=$?
    echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $tag"
    touch "$HERE/res/done_$tag"
  done
  # second starts for 40x79 at D 80 and 100: the 40x81 and 40x77 roots, resampled back to 40x79
  if [ $D = 80 ] || [ $D = 100 ]; then
    for G in 40x81 40x77; do
      src=$(printf "%s/res/Q_%s_D%s_D%.4f_%s.npz" "$HERE" "$G" "$D" "$D" "$G")
      tag=R_40x79_from${G#40x}_D$D
      [ -e "$src" ] || { echo "== no state $src"; continue; }
      [ -e "$HERE/res/done_$tag" ] && { echo "== skip $tag (done)"; continue; }
      echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC start $tag: 40x79 from $src"
      nice -n 10 $PY solver/rt/rt_run.py --start "$src" --grids 40x79 $OPTS --tol 1e-3 --out "$HERE/res" --tag "$tag"
      rc=$?
      echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC exit $rc $tag"
      touch "$HERE/res/done_$tag"
    done
  fi
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue done"
