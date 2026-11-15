#!/bin/bash
# #854's queue, one job at a time, 3 threads: the default's identity with #839 A_s1 (dz0 bit for bit against 4617f876,
# step 0's printed record), the option's first step, then the D 252.6 planted run with keep_projected (#713's flags,
# seed 1, the chain's own system), A_s1 its baseline.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
S=I603-win2/chain/anm_pin3_D252.6135.npz
DT=1.68453445011892229445312904531756908899422197089059690341775    # the truth's Delta, all eight parts
F="--threads 3 --switch 0 --reseed_o 3 --reseed_start pred --qd 0 --seed 1"
PY=/Users/nathan/venv-314/bin/python3
stamp() { echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: $*" >> "$D/queue.log"; }
stamp "queue started"
WT=839 bash "$D/run.sh" dz0_old octo_corrector.py planted "$RAW" $S $F --save_dz0 "$D/dz0_old.npz"
WT=854 bash "$D/run.sh" dz0_off octo_corrector.py planted "$RAW" $S $F --save_dz0 "$D/dz0_off.npz"
WT=854 bash "$D/run.sh" dz0_keep octo_corrector.py planted "$RAW" $S $F --keep_projected 1 --save_dz0 "$D/dz0_keep.npz"
{ "$PY" "$D/cmp_854.py" dz0 "$D/dz0_old.npz" "$D/dz0_off.npz"; echo "exit $?"
  "$PY" "$D/cmp_854.py" dz0 "$D/dz0_old.npz" "$D/dz0_keep.npz"; echo "exit $? (the control: must be 1)"; } > "$D/cmp_dz0.log" 2>&1
stamp "dz0 runs done"
WT=854 bash "$D/run.sh" off_step0 octo_corrector.py planted "$RAW" $S $F --it_max 1 --Delta_ref $DT --out "$D/off_step0"
{ "$PY" "$D/cmp_854.py" step0 "$RAW/I839-mac/A_s1_at_stop.log" "$D/off_step0.log"; echo "exit $?"
  "$PY" "$D/cmp_854.py" step0 "$RAW/I839-mac/A_s1_at_stop.log" "$D/off_step0.log" --mutate=digit
  echo "exit $? (the control: must be 1)"; } > "$D/cmp_step0.log" 2>&1
stamp "off_step0 done"
WT=854 bash "$D/run.sh" keep_s1 octo_corrector.py planted "$RAW" $S $F --keep_projected 1 --Delta_ref $DT \
    --out "$D/keep_s1"
stamp "keep_s1 done"
stamp "queue done"
