#!/bin/bash
# #641: the control (D 80, --kfreeze 3) and the eight runs (K = 9, 7 at D 80, 100, 150, 200), three at once, 2 threads each. --save_base 1 added to #603's flags
# so that the polished base is saved (eight parts) and Delta_base - Delta_state can be taken exactly (the log prints Delta to 18 digits and 5).
. /Users/nathan/Source/choptuik-large-d-raw-641/I641-macm3/common.sh
st() { case $1 in 80|100|150) echo T138-win2/chain/anm_pin3_D$1.0000.npz ;; 200) echo T138-win2/chain_o/anm_pin3_D200.0000.npz ;; esac; }
export -f run st; export RAWDIR FLAGS
for job in "3 80" "9 80" "7 80" "9 100" "7 100" "9 150" "7 150" "9 200" "7 200"; do echo $job; done |
  xargs -P 3 -L 1 bash -c '. /Users/nathan/Source/choptuik-large-d-raw-641/I641-macm3/common.sh; st() { case $1 in 80|100|150) echo T138-win2/chain/anm_pin3_D$1.0000.npz ;; 200) echo T138-win2/chain_o/anm_pin3_D200.0000.npz ;; esac; }; run $0 $1 $(st $1) 2'
