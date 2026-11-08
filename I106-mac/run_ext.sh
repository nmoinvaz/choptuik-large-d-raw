#!/bin/bash
# Issue #106, outside the criteria: the 40x79 continuation past D = 60 on the hp rows nearest each even integer from 62
# to 100 (dd to 66, pinned to 72, chain_fit from 74), as a test of the fits' extrapolation, which use D <= 60 only.
# Steps of 2 from 16:09 UTC (the first start, at 16:08 with steps of 1, was stopped during its first step to save time;
# cont/ext_step1_stopped.stdout).
# It waits for run_cont2.sh's path to end at 60.001952, then continues by rounds as run_cont2.sh does (newest saved
# state, the three before it as the cubic predictor's history, newton_tol 1e-36). There is no 32x101 state past 60 to
# restart from, so a failed step is retried once with the quadratic predictor, and a second failure stops the run.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --tol 1e-3 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
OPTS="$OPTS --newton_tol 1e-36"
PATHD="54.996085 56.01171 58.00599 60.001952 62.009781 64.009633 66.001705 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98 100"
S="$HERE/cont"
cd "$CODE" || exit 2
st() { printf "%s/cont_40x79_D%.4f_40x79.npz" "$S" "$1"; }
until grep -q "path done\|stopping" "$S/cont2.stdout" 2>/dev/null && ! pgrep -f "run_cont2.sh" > /dev/null; do
  sleep 30
done
grep -q "path done" "$S/cont2.stdout" || { echo "== run_cont2.sh did not finish its path; not extending"; exit 1; }
order=3
while true; do
  done_=(); todo=()
  for d in $PATHD; do if [ -e "$(st $d)" ]; then done_+=($d); else todo+=($d); fi; done
  [ ${#todo[@]} -eq 0 ] && { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC extension done"; break; }
  n=${#done_[@]}; last=${done_[$((n - 1))]}; next=${todo[0]}
  prev="$(st ${done_[$((n - 4))]}),$(st ${done_[$((n - 3))]}),$(st ${done_[$((n - 2))]})"
  ext=$(IFS=,; echo "${todo[*]}"); to=${todo[$((${#todo[@]} - 1))]}
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC round from $last to $to, predictor order $order"
  nice -n 10 $PY solver/rt/rt_run.py --start "$(st $last)" --start_prev "$prev" --grids 40x79 $OPTS --D_to "$to" \
      --dD 100 --pred_order $order --D_extra "$ext" --check_D "$ext" --out "$S" --tag ext_40x79
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC round exit $?"
  # rt_run.py names the states by its tag; give them the path's names
  for f in "$S"/ext_40x79_D*_40x79.npz; do [ -e "$f" ] && mv "$f" "$S/cont_${f##*/ext_}"; done
  if [ -e "$(st $next)" ]; then order=3; continue; fi
  if [ $order = 3 ]; then order=2; continue; fi
  echo "== D $next failed with both predictors; stopping"; break
done
