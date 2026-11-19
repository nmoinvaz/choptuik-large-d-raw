#!/bin/bash
# #980: launch one M = 9 run with level 5's approach radius XI ($1), 1 h cap, from solver/inner_stokes of the code worktree
XI=$1
INNER_NB_RTOL=1e-13 nohup python3 ~/Source/choptuik-large-d-raw/I980-rpi5/run_cap.py 1 logs/hier_nb_M9_app5_${XI}_rpi5.log logs/hier_nb_M9_app5_${XI}_rpi5.exit -- \
  ~/Source/venv-choptuik/bin/python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 \
  --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --verbose=2 --approach=5:${XI} > logs/run980_${XI}.driver.log 2>&1 &
