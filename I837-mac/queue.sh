#!/bin/bash
# #837's queue, one job at a time (run.sh NAME SCRIPT ARGS writes NAME.log)
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
S252=I603-win2/chain/anm_pin3_D252.6135.npz
S240=I603-win2/chain/anm_pin3_D240.1244.npz
# 1. the truth's residual and the first Newton step in the chain's own system (--tol 1e-100 forces the step)
for x in 252 240; do
  S=$([ $x = 252 ] && echo $S252 || echo $S240)
  bash "$D/run.sh" "step_D$x" octo_corrector.py planted "$RAW" $S --threads 3 --rel 0 --qd 0 --tol 1e-100 \
      --save_dz0 "$D/step_D${x}_dz0.npz" --out "$D/step_D$x"
done
# 2. the controls, each restoring one old behaviour; residual only (--od 0 --qd 0)
for x in 252 240; do
  S=$([ $x = 252 ] && echo $S252 || echo $S240)
  bash "$D/run.sh" "ctl_read4_D$x" octo_corrector.py planted "$RAW" $S --threads 3 --rel 0 --od 0 --qd 0 --read 4 \
      --out "$D/ctl_read4_D$x"
  bash "$D/run.sh" "ctl_heldfloat_D$x" octo_corrector.py planted "$RAW" $S --threads 3 --rel 0 --od 0 --qd 0 \
      --held float --out "$D/ctl_heldfloat_D$x"
  bash "$D/run.sh" "ctl_planstate_D$x" octo_corrector.py planted "$RAW" $S --threads 3 --rel 0 --od 0 --qd 0 \
      --plan state --out "$D/ctl_planstate_D$x"
done
# 3. the four-part states: the recorded runs' start lines, and #713's s0_D200 first step
bash "$D/run.sh" four_D200 octo_corrector.py planted "$RAW" T138-win2/chain_o/anm_pin3_D200.0000.npz --threads 3 \
    --switch 0 --reseed_o 3 --reseed_start pred --qd 0 --save_dz0 "$D/four_D200_dz0.npz"
bash "$D/run.sh" four_D180 octo_corrector.py planted "$RAW" T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 \
    --od 0 --qd 0
bash "$D/run.sh" four_D192 octo_corrector.py planted "$RAW" I13-win/chain_d6/anm_pin3_D192.0000.npz --threads 3 \
    --od 0 --qd 0
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: queue done" >> "$D/queue.log"
