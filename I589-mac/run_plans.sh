#!/usr/bin/env bash
# #589 step 1: each state saved with its run's plan, and its pinned max|F| on main's kernel and on cadcaf1's
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
C2=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i562/c2pkgs
R=$RAW/I589-mac
mkdir -p $R
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp || exit 9
run() {   # name, state, base ('' for the stored plan)
  local n=$1 st=$2 b=$3
  if [ -n "$b" ]; then
    nice -n 10 $PY -u plan_state.py $RAW $st --base $b --out I589-mac/$n.npz --threads 4 > $R/plan_main_$n.log 2>&1
  else
    nice -n 10 $PY -u plan_state.py $RAW $st --threads 4 > $R/plan_main_$n.log 2>&1
    cp $RAW/$st $R/$n.npz
  fi
  echo "plan_main_$n exit $?" >> $R/exits.txt
  PYTHONPATH=$C2 nice -n 10 $PY -u plan_state.py $RAW I589-mac/$n.npz --threads 4 > $R/plan_c2_$n.log 2>&1
  echo "plan_c2_$n exit $?" >> $R/exits.txt
}
run s215 I462-win/chain_d6/anm_pin3_D215.0000.npz I215-win/chain_d6/anm_pin3_D214.7500.npz
run s225 I461-win2/crawlB3/anm_pin3_D225.1312.npz I461-win2/crawlB2/anm_pin3_D215.1312.npz
run s235 I461-win2/crawlB5/anm_pin3_D235.1312.npz I461-win2/crawlB4/anm_pin3_D231.6312.npz
run s240 I461-win2/crawlJ/anm_pin3_D240.0258.npz ""
grep -h "pinned max" $R/plan_*.log
