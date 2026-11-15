#!/bin/bash
# stepbits.sh: Real's stored-step check four times, OPENBLAS_NUM_THREADS 1 and unset alternating, kernel threads 3
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
R=$S/raw781push
cd /Users/nathan/Source/choptuik-large-d-831/hp || exit 9
for env in 1 unset 1 unset; do
  if [ "$env" = 1 ]; then
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 /Users/nathan/venv-314/bin/python3 -u $S/i831/stepbits.py $R I823-mac/dz0_truth.npz I603-win2/chain/anm_pin3_D252.6135.npz 3
  else
    env -u OPENBLAS_NUM_THREADS PYTHONPATH=$SITE nice -n 10 /Users/nathan/venv-314/bin/python3 -u $S/i831/stepbits.py $R I823-mac/dz0_truth.npz I603-win2/chain/anm_pin3_D252.6135.npz 3
  fi
done
echo "exit $?"
