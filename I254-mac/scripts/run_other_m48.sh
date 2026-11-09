#!/bin/bash
# The other M 48 runs on the large-D layout, from the worktree root, one process:
# (a) M 48 re-converged as gamma_dd.py does, on the layouts of review R2 (D 60, hp/review/rv2_resolve_D60.jsonl) and
#     hp/data/large_d (checks.jsonl at D 65.01; m48_diag.jsonl at D 67.72 with ks 200);
# (b) hp/resolution_check.py's states (resolution-mac/), resampled to M 48 only (that path solves a pinned
#     quad-double system; the dd measure here is of its start), kf from the state (3 for the chain, 13 otherwise);
# (c) the D 45.05 M 48 kf 21 mode-count background (I170-macm3), refitted (--fit) and re-converged, for Delta's change.
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
O=$RAW/I254-mac
run() { caffeinate -i nice -n 10 $PY hp/series_truncation.py "$@"; echo "$2 exit $?" >> $O/logs/other_exits.txt; }
run $O/other_m48.jsonl hp/data/states/up13_D60.0020.npz --Mhi=48 --fit --save=$O/states --tag=rv2_D60_M48 \
  > $O/logs/other_rv2_D60.log 2>&1
run $O/other_m48.jsonl hp/data/large_d/up70_D65.0117.npz --Mhi=48 --fit --save=$O/states --tag=large_d_checks_M48 \
  > $O/logs/other_D65.0117.log 2>&1
run $O/other_m48.jsonl hp/data/large_d/up70_D67.7224.npz --ks=200 --Mhi=48 --fit --save=$O/states \
  --tag=large_d_m48_diag > $O/logs/other_D67.7224.log 2>&1
for s in hp/data/large_d/up70_D61.6587.npz hp/data/large_d/up70_D64.3869.npz hp/data/large_d/up70_D66.5830.npz \
         hp/data/large_d/up70_D67.7899.npz $RAW/T81/conv_pin5_D73.0000_D73.000000.npz \
         $RAW/T138-win2/chain/anm_pin3_D80.0000.npz $RAW/T138-win2/chain/anm_pin3_D100.0000.npz \
         $RAW/T138-win2/chain/anm_pin3_D150.0000.npz $RAW/T138-win2/chain_o/anm_pin3_D200.0000.npz; do
  run $O/resolution_m48.jsonl $s --Mhi=48 --resample_only --tag=resolution_check \
    >> $O/logs/resolution_m48.log 2>&1
done
run $O/other_m48.jsonl $RAW/I170-macm3/hp_data_after/modecount_state_D45.0507_M48_kf21.npz --fit \
  --tag=modecount_D45_kf21_fit > $O/logs/fit_D45_kf21.log 2>&1
