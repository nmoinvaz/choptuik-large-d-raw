#!/usr/bin/env bash
# #589 step 2: on cadcaf1 (eight-part projector), near_null (main d020d58, stored plan) and held_homotopy's probe at
# each state saved with its run's plan; one job at a time, 4 threads, nice 10
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
MAINHP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i589/mainhp/hp
MYHP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp
R=$RAW/I589-mac
for n in ${@:-s240 s235 s225 s215}; do
  cd $MYHP || exit 9
  $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/c2_probe_$n.log
  nice -n 10 $PY -u held_homotopy.py $RAW I589-mac/$n.npz $R/c2_probe_$n --mode real --threads 4 --probe_only 1 --ladder 0:90:2 >> $R/c2_probe_$n.log 2>&1
  echo "c2_probe_$n exit $? $(date -u '+%H:%M:%S')" >> $R/exits.txt
  cd $MAINHP || exit 9
  $PY -c "import hpkernel; print('hpkernel', hpkernel.__file__)" > $R/c2_nn_$n.log
  nice -n 10 $PY -u near_null.py $RAW I589-mac/$n.npz --threads=4 --json=$R/c2_nn_$n.json >> $R/c2_nn_$n.log 2>&1
  echo "c2_nn_$n exit $? $(date -u '+%H:%M:%S')" >> $R/exits.txt
done
