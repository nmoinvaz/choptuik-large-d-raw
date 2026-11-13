#!/bin/zsh
# #693 on the Mac: from the worktree's hp/ directory. RAW is the raw-data clone, HP the hp/ directory of choptuik-large-d.
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i693/raw
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ac6dd6142bb1fca1c/hp
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
export OPENBLAS_NUM_THREADS=1
PY="nice -n 10 /Users/nathan/venv-314/bin/python3"
O=$RAW/I693-mac
cd $HP
STATES=("${(@f)$(sed "s|^|$RAW/I603-win2/|" $O/states.txt)}")
step() { local name=$1; shift; "$@"; echo "$name exit $?" >> $O/exits_693.txt; }
case $1 in
  checks)
    step selftest eval "$PY horizon_radius.py selftest > $O/selftest.log 2>&1"
    step selftest_drop_term eval "$PY horizon_radius.py selftest --mutate drop_term > $O/selftest_drop_term.log 2>&1"
    step control_D253.7313 eval "$PY horizon_radius.py control $RAW/I603-win2/chain/anm_pin3_D253.7313.npz > $O/control_D253.7313.log 2>&1"
    step control_D253.7313_shift eval "$PY horizon_radius.py control $RAW/I603-win2/chain/anm_pin3_D253.7313.npz --mutate shift > $O/control_D253.7313_shift.log 2>&1"
    step control_D226.1312 eval "$PY horizon_radius.py control $RAW/I603-win2/chain/anm_pin3_D226.1312.npz > $O/control_D226.1312.log 2>&1"
    ;;
  onsol)
    step onsol eval "$PY -u horizon_radius.py run $O/onsol.jsonl ${STATES[*]} --kmax 160 --precs dd,dd1,qd,od --deltas 0 --coef $O/coef > $O/onsol.log 2>&1"
    ;;
  long)
    step long eval "$PY -u horizon_radius.py run $O/long.jsonl $RAW/I603-win2/base/base_pin3_D225.1312.npz $RAW/I603-win2/chain/anm_pin3_D253.7313.npz --kmax 300 --precs qd --deltas 0 --coef $O/coef_long > $O/long.log 2>&1"
    ;;
  long_all)
    step long_all eval "$PY -u horizon_radius.py run $O/long_all.jsonl ${STATES[*]} --kmax 300 --precs qd --deltas 0 --coef $O/coef_long_all > $O/long_all.log 2>&1"
    ;;
  long_od)
    step long_od eval "$PY -u horizon_radius.py run $O/long_od.jsonl $RAW/I603-win2/chain/anm_pin3_D253.7313.npz --kmax 240 --precs od --deltas 0 --coef $O/coef_long_od > $O/long_od.log 2>&1"
    ;;
  pdelta)
    PAIRS=()
    for P in $RAW/I603-win2/chain/pred_pin3_D*.npz $RAW/I603-win2/chain_nat/pred_pin3_D*.npz; do
      S=${P/pred_pin3/anm_pin3}
      [[ -f $S ]] && PAIRS+=($P $S)
    done
    step pdelta eval "$PY horizon_radius.py pdelta ${PAIRS[*]} --reseed $RAW/I603-win2/chain/anm_run.jsonl --reseed $RAW/I603-win2/chain_nat/anm_run.jsonl > $O/pdelta.log 2>&1"
    ;;
  polish4)
    for P in chain/pred_pin3_D249.3927 chain_nat/pred_pin3_D253.7591 chain_nat/pred_pin3_D253.7869; do
      S=${P/pred_pin3/anm_pin3}
      step polish4_${P:t} eval "$PY -u horizon_radius.py polish4 $RAW/I603-win2/$P.npz $RAW/I603-win2/$S.npz >> $O/polish4.log 2>&1"
    done
    ;;
  summary)
    step summary eval "$PY horizon_radius.py summary $O/onsol.jsonl $O/law.jsonl --reseed $RAW/I603-win2/chain/anm_run.jsonl --reseed $RAW/I603-win2/chain_nat/anm_run.jsonl --coef $O/coef > $O/summary.log 2>&1"
    step summary_long eval "$PY horizon_radius.py summary $O/long.jsonl --coef $O/coef_long > $O/summary_long.log 2>&1"
    step summary_long_all eval "$PY horizon_radius.py summary $O/long_all.jsonl --coef $O/coef_long_all > $O/summary_long_all.log 2>&1"
    step summary_long_od eval "$PY horizon_radius.py summary $O/long_od.jsonl --coef $O/coef_long_od > $O/summary_long_od.log 2>&1"
    step csv eval "$PY horizon_radius.py csv $HP/data/horizon_radius.csv $O/onsol.jsonl $O/law.jsonl --coef $O/coef --long $O/long_all.jsonl --coef_long $O/coef_long_all > $O/csv.log 2>&1"
    ;;
  ladder)
    for P in chain/pred_pin3_D226.1312 chain/pred_pin3_D249.0113 chain/pred_pin3_D249.3927 chain_nat/pred_pin3_D253.7591 chain_nat/pred_pin3_D253.7869 chain_nat/pred_pin3_D253.8043; do
      S=${P/pred_pin3/anm_pin3}
      step ladder_${P:t} eval "$PY -u horizon_radius.py ladder $RAW/I603-win2/$P.npz $RAW/I603-win2/$S.npz >> $O/ladder.log 2>&1"
    done
    ;;
  law)
    LAWS=($RAW/I603-win2/base/base_pin3_D225.1312.npz $RAW/I603-win2/chain/anm_pin3_D231.1312.npz $RAW/I603-win2/chain/anm_pin3_D237.1312.npz
          $RAW/I603-win2/chain/anm_pin3_D241.9602.npz $RAW/I603-win2/chain/anm_pin3_D244.6366.npz $RAW/I603-win2/chain/anm_pin3_D247.0429.npz
          $RAW/I603-win2/chain/anm_pin3_D249.0113.npz $RAW/I603-win2/chain/anm_pin3_D249.8696.npz $RAW/I603-win2/chain/anm_pin3_D251.3038.npz
          $RAW/I603-win2/chain/anm_pin3_D252.6135.npz $RAW/I603-win2/chain/anm_pin3_D253.6411.npz $RAW/I603-win2/chain_nat/anm_pin3_D253.8043.npz)
    step law eval "$PY -u horizon_radius.py run $O/law.jsonl ${LAWS[*]} --kmax 160 --precs qd --deltas 1e-40,1e-36,1e-32,1e-28,1e-24,1e-20 --coef $O/coef > $O/law.log 2>&1"
    ;;
esac
