#!/bin/bash
# gamma_dd.py --M48's states (records hp/data/gamma_dd.jsonl and hp/data/local/gamma_dd.jsonl): each M 32 state
# polished as gamma_batch.py does (--polish=4), resampled to M 48 and re-converged as gamma_dd.py does, lam located
# on both, and where a series is above the gate, the layout refitted and re-solved (--fit). From the worktree root.
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw/I254-mac
for st in up2_D20.0437 up6_D30.0688 up7_D40.0201 up8_D50.0075; do
  caffeinate -i nice -n 10 $PY hp/series_truncation.py $RAW/gamma_m48.jsonl hp/data/states/$st.npz --polish=4 \
    --Mhi=48 --lam --fit --save=$RAW/states --tag=gamma_dd_M48 > $RAW/logs/gamma_m48_$st.log 2>&1
  echo "$st exit $?" >> $RAW/logs/gamma_m48_exits.txt
done
