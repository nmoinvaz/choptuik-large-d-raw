#!/bin/bash
# the checks after step 0, in order: step 0d (plain octo Newton from 188.0246), (e) before and after, (a), (b), (c)
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
R=/Users/nathan/Source/choptuik-large-d-raw
H=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp
for job in "$@"; do
  case $job in
    od188) cd $H && $PY -u $A/step0_od.py $R 1e-32 T129-win2/chain/anm_pin3_D188.0246.npz > $A/step0_od188.log 2>&1 ;;
    od194) cd $H && $PY -u $A/step0_od.py $R 1e-32 T129-win2/chain2/anm_pin3_D193.7746.npz > $A/step0_od194.log 2>&1 ;;
    e_before) bash $A/run_e.sh before > $A/e_before.log 2>&1 ;;
    e_after) bash $A/run_e.sh after > $A/e_after.log 2>&1 ;;
    a) cd $H && $PY -u octo_corrector.py planted $R T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 --out $A/check_a > $A/check_a.log 2>&1 ;;
    a_qd) cd $H && $PY -u octo_corrector.py planted $R T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 --od 0 --Delta_ref 1.700531269818162204386381037834122353007 --out $A/check_a_qd > $A/check_a_qd.log 2>&1 ;;
    c) cd $H && $PY -u octo_corrector.py planted $R T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 --qd 0 --mutate_offset qd --Delta_ref 1.700531269818162204386381037834122235155 --out $A/check_c > $A/check_c.log 2>&1 ;;
    b) cd $H && $PY -u octo_corrector.py wall $R T129-win2/chain2/pred_pin3_D194.2746.npz --threads 3 --qd 0 --out $A/check_b > $A/check_b.log 2>&1 ;;
  esac
  echo "$job exit $?" >> $A/checks_status.log
done
