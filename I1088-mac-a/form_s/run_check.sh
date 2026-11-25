#!/bin/bash
# form S's validation on the Mac (#1088): the checks at D 16.76-27.04 against form A and delta_all.csv, the flux
# control, the planted check and its control. Args: CODE (worktree), SITE (the dev-o1 build of wip/large-d-form-s).
{
set -u
CODE=$1; SITE=$2; HERE=$(cd "$(dirname "$0")" && pwd)
cd "$CODE/hp" || exit 1
export PYTHONPATH=$SITE OPENBLAS_NUM_THREADS=2
PY=/Users/nathan/venv-314/bin/python
date -u '+start %Y-%m-%d %H:%M:%S UTC'
nice -n 10 $PY -u form_s.py check data/states/up2_D16.7600.npz data/states/up2_D20.0437.npz data/states/up3_D23.0433.npz \
  data/states/up4_D26.0797.npz data/states/up6_D27.0422.npz --threads 2 --out "$HERE/states" > "$HERE/check.log" 2>&1
nice -n 10 $PY -u form_s.py check data/states/up2_D20.0437.npz --threads 2 --mutate flux > "$HERE/check_flux.log" 2>&1
nice -n 10 $PY -u form_s.py planted "$HERE/states/s_D20.0437.npz" --threads 2 > "$HERE/planted.log" 2>&1
nice -n 10 $PY -u form_s.py planted "$HERE/states/s_D20.0437.npz" --threads 2 --mutate step > "$HERE/planted_step.log" 2>&1
date -u '+end %Y-%m-%d %H:%M:%S UTC'
exit
}
