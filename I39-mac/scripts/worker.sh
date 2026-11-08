#!/bin/zsh
# one review worker: for each row of $ROWS not yet claimed, regenerate its disc inputs (original code) if missing, then
# run the review's disc check on them. Two workers with opposite row orders share the rows through lock directories.
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
PY=/Users/nathan/venv-qd/bin/python
mkdir -p $S/locks
for j in ${(s:,:)ROWS}; do
  mkdir $S/locks/row_$j 2>/dev/null || continue
  jj=$(printf '%02d' $j)
  if [ ! -f $O/disc_inputs/row_$jj.json ]; then
    nice -n 10 $PY -u $R/dump_inputs.py --ray=$S/rerun_rows --out=$O/disc_inputs --rows=$j >> $O/dump_inputs_$NAME.log 2>&1
  fi
  if [ ! -f $O/check_6b1/row_$jj.json ]; then
    nice -n 10 $PY -u $R/check_6b1.py discs --inputs=$O/disc_inputs --rows=$j --out=$O/check_6b1 >> $O/check_6b1_$NAME.log 2>&1
    echo "row $j check exit $?" >> $O/check_6b1_$NAME.log
  fi
done
echo "worker $NAME done $(date -u '+%H:%M')" >> $O/check_6b1_$NAME.log
