#!/bin/bash
{
L=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/r3fix
PY=/Users/nathan/venv-314/bin/python
cd /Users/nathan/Source/choptuik-route3fix/solver/proof || exit 1
run() { name=$1; shift; s=$(date -u +%s); timeout 1800 nice -n 10 $PY "$@" > $L/$name.log 2>&1; rc=$?; echo "$name exit $rc $(( $(date -u +%s) - s )) s $(date -u '+%H:%M:%S')" >> $L/exits.txt; }
run outward outward.py
run outward_mut outward.py --mutate=nearest
run bound_constants route3_bound.py --constants
run bound_constants_J100 route3_bound.py --constants --J0=100
run head_certify route3_head.py --certify
run head_check route3_head.py --check
echo done >> $L/exits.txt
exit
}
