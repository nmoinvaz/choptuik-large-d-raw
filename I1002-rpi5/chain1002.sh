#!/bin/bash
# #1002: the five groups of eight perturbed solves, rtol 1e-14, two solves side by side (run from solver/inner_stokes of the code worktree)
export INNER_NB_RTOL=1e-14
P=~/Source/venv-choptuik/bin/python
D=~/Source/choptuik-large-d-raw/I1002-rpi5/run_pert1002.py
W977=/home/nathan/Source/choptuik-large-d-raw-964/I977-win2/logs/hier_nb_M7_win2_rtol14_s977_xi015
W989=/home/nathan/Source/choptuik-large-d-raw-964/I989-win2/logs/hier_nb_M7_win2_rtol14_xi0145
$P $D --end ${W977}_zero.log --xi1 0.15  --seeds 1020-1027 --tag rtol14_xi0150_zero --cap_h 3
$P $D --end ${W977}_dA.log   --xi1 0.15  --seeds 1030-1037 --tag rtol14_xi0150_dA --A 2.719419 --cap_h 3
$P $D --end ${W977}_dw.log   --xi1 0.15  --seeds 1040-1047 --tag rtol14_xi0150_dw --w 1.000122 --cap_h 3
$P $D --end ${W989}_dA.log   --xi1 0.145 --seeds 1000-1007 --tag rtol14_xi0145_dA --A 2.719419 --cap_h 3
$P $D --end ${W989}_dw.log   --xi1 0.145 --seeds 1010-1017 --tag rtol14_xi0145_dw --w 1.000122 --cap_h 3
