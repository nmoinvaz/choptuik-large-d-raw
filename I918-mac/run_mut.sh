#!/bin/bash
# #918: check (2) and the seven mutations of mode_check.py at one state. Each mutation must exit 1.
# (Its first version wrote "exit $?" after a command substitution, which logged date's status, 0, for every
# mutation of the D 9 run; out/mutations.txt was rebuilt from the statuses in out/gate.log.)
J=$(cd "$(dirname "$0")" && pwd)
ST=$1; NAME=$2
bash "$J/run_check.sh" "$ST" "${NAME}_c2" --only 2
for m in sigma_h real_solve vtau rate_horizon rate_lu rate_centre rate_steps; do
    bash "$J/run_check.sh" "$ST" "${NAME}_mut_$m" --mutate $m
    rc=$?
    echo "$(date -u '+%F %T') UTC mutation $m at $NAME: exit $rc (1 expected)" >> "$J/out/mutations.txt"
done
echo "$(date -u '+%F %T') UTC run_mut $NAME done" >> "$J/out/gate.log"
