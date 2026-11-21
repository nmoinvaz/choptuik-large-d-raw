#!/bin/bash
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1035c
O=$S/out
cd /Users/nathan/Source/choptuik-large-d-fh2/hp
PY=/Users/nathan/venv-314/bin/python
ST=$S/states/I966-dh370_ks_chain3b_leg14_D261.1415_ks293_anm_pin3_D262.0099.npz
run() { name=$1; shift; echo "$(date -u '+%H:%M:%S') start $name" >> $O/queue.log; nice -n 10 $PY factored_horizon.py "$@" --out $O/$name.json > $O/$name.log 2>&1; rc=$?; echo "$(date -u '+%H:%M:%S') end $name exit $rc" >> $O/queue.log; }
run raisecheck_a_D262 raisecheck $ST --ks 315 --prec 512 --cache $O/rung_cols_D262_ks315.json --rows a
run raisecheck_ma_D262 raisecheck $ST --ks 315 --prec 512 --cache $O/rung_cols_D262_ks315.json --rows ma
echo "$(date -u '+%H:%M:%S') queue done" >> $O/queue.log
exit
}
