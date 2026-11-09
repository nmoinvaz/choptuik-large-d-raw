#!/bin/bash
# #257: the four M 48 circles whose alias-rule replay needs new determinants, on their stored backgrounds, #178's two
# R 0.03 circles first. From the code worktree's root; one process; modecount_cx from the main checkout's build.
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
O=$RAW/I257-mac
export PYTHONPATH=/Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build
L() { caffeinate -i nice -n 10 $PY $O/scripts/live_circles.py hp "$@"; echo "$2 $5 exit $?" >> $O/logs/live_exits.txt; }
L $RAW/I178-macm3/locate_r2/modecount_state_D45.0507_M48_kf21.npz 21 \
  $RAW/I178-macm3/locate_r2/modecount_D45.0507_M48_kf21_locr2_evals.jsonl $O/live/I178_locr2 \
  1.14,0,0.03,16 1.2,0,0.03,16 > $O/logs/live_I178_locr2.log 2>&1
L $RAW/I238-macm3/D55/hp_data_after/modecount_state_D55.0351_M48_kf23.npz 23 \
  $RAW/I238-macm3/D55/data/modecount_D55.0351_M48_kf23_evals.jsonl $O/live/I238_D55 \
  0.07342,3.8388,0.3,20 > $O/logs/live_I238_D55.log 2>&1
L $RAW/I212-macm3/hp_data_after/modecount_state_D61.0264_M48_kf23.npz 23 \
  $RAW/I230-mac/data/modecount_D61.0264_M48_kf23_B_evals.jsonl $O/live/I230_kf23_B \
  3.01943,0,0.2,20 > $O/logs/live_I230_kf23_B.log 2>&1
