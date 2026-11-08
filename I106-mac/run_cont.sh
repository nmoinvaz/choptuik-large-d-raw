#!/bin/bash
# Issue #106: the 40x79 continuation (EEG's 40 x 80) on the hp rows nearest each integer D, cubic predictor.
#   run_cont.sh LEG
# LEG 1: D 20.043653 -> 53.991398 at newton_tol 1e-40, from I105-mac's 32x81 state (prev 17, 18, 19), resampled.
# LEG 2: D 54.996085 -> 60.001952 at newton_tol 1e-36, from leg 1's last states.
# Output in cont/ beside this script (tag cont_40x79, appended).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
RAW="$(cd "$HERE/.." && pwd)"
CODE=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-abc971b3baa37717c
LEG="$1"
P1=20.991519,21.912601,23.043278,23.952249,25.07972,26.07972,26.983581,27.95546,28.99264,29.984746,30.987328,32.021319
P1=$P1,32.987798,33.991236,34.993266,35.953229,36.965729,38.020417,39.001863,40.020065,40.952548,42.04394,42.998908
P1=$P1,43.98116,44.963411,46.001135,47.008218,48.015301,49.022384,50.007491,50.980148,51.991398,52.991398,53.991398
P2=54.996085,56.01171,56.99989,58.00599,58.99805,60.001952
C="$RAW/I105-mac/cont"
if [ "$LEG" = 1 ]; then
  START="$C/cont_32x81_D20.0437_32x81.npz"
  PREV="$C/cont_32x81_D17.0000_32x81.npz,$C/cont_32x81_D18.0000_32x81.npz,$C/cont_32x81_D19.0000_32x81.npz"
  EXTRA=$P1; DTO=53.991398; NT=1e-40
else
  S="$HERE/cont"
  START="$S/cont_40x79_D53.9914_40x79.npz"
  PREV="$S/cont_40x79_D50.9801_40x79.npz,$S/cont_40x79_D51.9914_40x79.npz,$S/cont_40x79_D52.9914_40x79.npz"
  EXTRA=$P2; DTO=60.001952; NT=1e-36
fi
mkdir -p "$HERE/cont"
cd "$CODE" || exit 2
export MULTIDOUBLE_SITE=/Users/nathan/Source/venv-anm/lib/python3.13/site-packages
exec nice -n 10 /Users/nathan/venv-qd/bin/python solver/rt/rt_run.py --start "$START" --start_prev "$PREV" \
    --grids 40x79 --solver mp --D_to "$DTO" --dD 100 --pred_order 3 --D_extra "$EXTRA" --check_D "$EXTRA,20.043653" \
    --tol 1e-4 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol "$NT" \
    --out "$HERE/cont" --tag cont_40x79
