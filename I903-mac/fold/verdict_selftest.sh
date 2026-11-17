#!/bin/bash
# end-to-end controls of fold_est_903.py verdict on synthetic chain folders with a known fold (#903)
SP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad
PY=/Users/nathan/venv-314/bin/python; F=$SP/i903/fold_est_903.py; RAW=$SP/raw-wt; T=$SP/i903/fold/synth
export PYTHONPATH=/Users/nathan/Source/choptuik-large-d-xf-903/hp
B=258.13125,259.13125,259.6
for s in 0 0.03 -0.06 0.06; do
  d=$T/shift_$s
  $PY $F mkplant $d --shift=$s --bases=$B
  $PY -u $F verdict $d $RAW --json=$T/verdict_shift_$s.json > $T/verdict_shift_$s.log 2>&1; echo "shift $s: exit $?"
  grep "^control\|^stop\|^shift\|^matched" $T/verdict_shift_$s.log
done
d=$T/notyet; $PY $F mkplant $d --shift=0 --bases=258.13125,259.13125
$PY -u $F verdict $d $RAW > $T/verdict_notyet.log 2>&1; echo "not yet: exit $?"; grep "^stop\|^shift" $T/verdict_notyet.log
