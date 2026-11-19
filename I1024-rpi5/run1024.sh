#!/bin/bash
# #1024 on rpi5: the 17 listed runs (+ one extra), one at a time, nice 10, each with its expected exit code. setsid nohup bash run1024.sh > logs/driver.log 2>&1 &
set -u
R=$(cd "$(dirname "$0")" && pwd); PY=$HOME/Source/venv-choptuik/bin/python
cd $HOME/Source/choptuik-large-d-964/solver/proof/review_p2c || exit 9
echo "$(date -u '+%F %T UTC') start, code $(git rev-parse --short HEAD)" | tee $R/logs/exits.txt
run() { local name=$1 exp=$2 script=$3; shift 3; local t0=$(date +%s)
  nice -n 10 timeout 2h $PY -u $script "$@" > $R/logs/$name.log 2>&1; local rc=$?
  echo "$name exit $rc expected $exp $([ $rc -eq $exp ] && echo OK || echo MISMATCH) $(( $(date +%s) - t0 )) s" | tee -a $R/logs/exits.txt; }
run disc_checkeq 0 p2c_disc.py --checkeq
run disc_checkint 0 p2c_disc.py --checkint
run disc_ray 0 p2c_disc.py --discs=ray --out=$R
run disc_K1_toolarge 1 p2c_disc.py --discs=11:0 --radius=16 --out=$R
run disc_K2_sign 1 p2c_disc.py --discs=ray --mutate=sign --out=$R
run h8_centre 0 p2c_h8.py --centre
run h8_centre_mut_A 1 p2c_h8.py --centre --mutate=A
run h8_d0_0 0 p2c_h8.py --d0=0 --out=$R
run h8_d0_1e7 0 p2c_h8.py --d0=1e7 --out=$R
run h8_d0_0_mut_sign 1 p2c_h8.py --d0=0 --mutate=sign
run b5_model 0 p2c_b5.py --model
run b5_phiz 0 p2c_b5.py --phiz
run b5_residual 0 p2c_b5.py --residual
run b5_phiz_mut_G0 1 p2c_b5.py --phiz --mutate=G0
run b5_residual_mut_offphi 1 p2c_b5.py --residual --mutate=offphi
run b5_sector_box 0 p2c_b5.py --sector --box
run b5_sector_box_nr32_na64 0 p2c_b5.py --sector --box --nr=32 --na=64 --out=$R
run disc_all_infl2 0 p2c_disc.py --discs=all --infl=2 --tag=all_infl2 --out=$R
echo "$(date -u '+%F %T UTC') end" | tee -a $R/logs/exits.txt
