#!/bin/bash
# Issue #106: the 40x79 continuation with restarts, replacing run_cont.sh from 14:20 UTC. run_cont.sh leg 1's step
# 21.912601 -> 23.043278 did not converge; its cubic predictor ran through a resampled 32x81 state (D = 19), and the
# 40x79 root at 23.043278 exists (diag/d23_from101: from I105-mac's 32x101 state at D = 23, Delta 1.29e-9 below hp).
# Each round continues from the newest saved path state, with the three before it as the predictor's history (40x79
# roots only). When a step fails, that D is solved directly from the nearest 32x101 state of I105-mac (D <= 30) or
# I145-mac (D > 30), resampled (rt_run.py --start S --D_start D), into cont/ with the same tag, and the next round goes
# on from there. Newton's target is 1e-40 below D = 54 and 1e-36 from 54.996085 (the criteria). A D that fails both
# ways stops the loop.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW="$(cd "$HERE/.." && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
PY=/Users/nathan/venv-qd/bin/python
OPTS="--solver mp --tol 1e-4 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4"
PATHD="20.043653 20.991519 21.912601 23.043278 23.952249 25.07972 26.07972 26.983581 27.95546 28.99264 29.984746
30.987328 32.021319 32.987798 33.991236 34.993266 35.953229 36.965729 38.020417 39.001863 40.020065 40.952548 42.04394
42.998908 43.98116 44.963411 46.001135 47.008218 48.015301 49.022384 50.007491 50.980148 51.991398 52.991398 53.991398
54.996085 56.01171 56.99989 58.00599 58.99805 60.001952"
S="$HERE/cont"
cd "$CODE" || exit 2
st() { printf "%s/cont_40x79_D%.4f_40x79.npz" "$S" "$1"; }
ntol() { awk -v d="$1" 'BEGIN { print (d > 54.5 ? "1e-36" : "1e-40") }'; }
# the D = 23.043278 root of the diagnosis, as the first restart's start
[ -e "$(st 23.043278)" ] || cp "$HERE/diag/d23_from101_D23.0433_40x79.npz" "$(st 23.043278)"
while true; do
  done_=(); todo=()
  for d in $PATHD; do if [ -e "$(st $d)" ]; then done_+=($d); else todo+=($d); fi; done
  [ ${#todo[@]} -eq 0 ] && { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC path done"; break; }
  n=${#done_[@]}; last=${done_[$((n - 1))]}; next=${todo[0]}
  prev="$(st ${done_[$((n - 4))]}),$(st ${done_[$((n - 3))]}),$(st ${done_[$((n - 2))]})"
  nt=$(ntol $next)
  # this round's targets: the remaining D with the same Newton target as the next one
  ext=""; to=""
  for d in "${todo[@]}"; do [ "$(ntol $d)" = "$nt" ] && { ext="$ext,$d"; to=$d; }; done
  ext=${ext#,}
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC round from $last to $to, newton_tol $nt"
  nice -n 10 $PY solver/rt/rt_run.py --start "$(st $last)" --start_prev "$prev" --grids 40x79 $OPTS --D_to "$to" \
      --dD 100 --pred_order 3 --D_extra "$ext" --check_D "$ext" --newton_tol "$nt" --out "$S" --tag cont_40x79
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC round exit $?"
  [ -e "$(st $next)" ] && continue
  # the next D failed: solve it directly from the nearest 32x101 state
  src=$($PY - "$next" "$RAW" <<'EOF'
import sys, glob, re
D, raw = float(sys.argv[1]), sys.argv[2]
fs = glob.glob(raw + "/I105-mac/cont/cont_32x101_D*_32x101.npz") if D <= 30.5 else \
    glob.glob(raw + "/I145-mac/cont/cont_32x101_D*_32x101.npz")
print(min(fs, key=lambda f: abs(float(re.search(r"_D([0-9.]+)_32x101", f).group(1)) - D)))
EOF
)
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC direct solve at $next from $src"
  nice -n 10 $PY solver/rt/rt_run.py --start "$src" --D_start "$next" --grids 40x79 $OPTS --newton_tol "$nt" \
      --out "$S" --tag cont_40x79
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC direct exit $?"
  if [ ! -e "$(st $next)" ] || ! tail -1 "$S/cont_40x79.jsonl" | grep -q '"ok": true'; then
    [ -e "$(st $next)" ] && mv "$(st $next)" "$(st $next).failed"     # rt_run.py saves a start state even unsolved
    echo "== D $next failed both ways; stopping"; break
  fi
done
