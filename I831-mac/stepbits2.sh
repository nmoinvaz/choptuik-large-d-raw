#!/bin/bash
# stepbits2.sh: the check with reseed imported before Real, as #828's probe did: on the old reseed (the 828 worktree,
# reseed sets 50 digits on import) and on the fixed one (831), OPENBLAS_NUM_THREADS=1, kernel threads 3
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
R=$S/raw781push
while pgrep -f "i831/stepbits.sh" > /dev/null; do sleep 10; done
for wt in 828 831; do
  cd /Users/nathan/Source/choptuik-large-d-$wt/hp || exit 9
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 /Users/nathan/venv-314/bin/python3 -u $S/i831/stepbits.py $R I823-mac/dz0_truth.npz I603-win2/chain/anm_pin3_D252.6135.npz 3 reseed_first
done
echo "exit $?"
