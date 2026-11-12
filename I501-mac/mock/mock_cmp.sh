#!/usr/bin/env bash
# Mock-solver output of the rebased near_null.py against 9e21ed8's, for the default, planted and control paths.
# Usage: mock_cmp.sh HP
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i501
HP=$1
PY=/Users/nathan/venv-314/bin/python
for args in "" "--planted=1 --w=1e-2" "--planted=1 --w=1e-2 --mutate=scale_block" "--mutate=sigma" "--mutate=scale_p1"; do
  # shellcheck disable=SC2086
  PYTHONPATH=$S/old $PY $S/mock_run_old.py "$HP" $args > $S/mock_old.txt 2>&1
  # shellcheck disable=SC2086
  $PY $S/mock_run.py "$HP" $args > $S/mock_new.txt 2>&1
  if cmp -s $S/mock_old.txt $S/mock_new.txt; then echo "identical: [$args] ($(wc -l < $S/mock_new.txt) lines, $(tail -1 $S/mock_new.txt))"; else echo "DIFFER: [$args]"; diff $S/mock_old.txt $S/mock_new.txt | head; fi
done
