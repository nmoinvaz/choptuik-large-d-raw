#!/bin/bash
# Own-M truncation of every state in the given lists (lists/<group>.txt), one process, from the worktree root.
#   bash run_sweeps.sh GROUP [GROUP ...]
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw/I254-mac
for g in "$@"; do
  caffeinate -i nice -n 10 $PY hp/series_truncation.py $RAW/sweep_$g.jsonl $(cat $RAW/lists/$g.txt) --tag=$g \
    > $RAW/logs/sweep_$g.log 2>&1
  echo "$g exit $?" >> $RAW/logs/sweep_exits.txt
done
