#!/bin/bash
# The control of hp/series_truncation.py and its mutation, run from the code worktree's root.
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
L=$RAW/I254-mac/logs
nice -n 10 $PY hp/series_truncation.py --selftest --raw=$RAW > $L/selftest.log 2>&1
echo "exit $?" >> $L/selftest.log
nice -n 10 $PY hp/series_truncation.py --selftest --raw=$RAW --mutate=half > $L/selftest_mutate_half.log 2>&1
echo "exit $?" >> $L/selftest_mutate_half.log
tail -2 $L/selftest.log $L/selftest_mutate_half.log
