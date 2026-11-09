#!/bin/bash
# #250's runs, in order (criteria in ../README.md). Run from anywhere: caffeinate -i nice -n 10 bash run.sh
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I250-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ) main $(git -C $HP rev-parse HEAD)" >> $F/exits.txt

# 5. determinant check of the inner-node state
$PY $F/../I252-mac/scripts/det_check.py $HP $F/states/modecount_state_D30.0688_M48_inner015.npz none 2.0797477104405484 \
    $F/det_check_inner015.json > $F/det_check_inner015.log 2>&1
ex det_check_inner015 $?

# 1 and 2. the circle at the pair and the lambda_phys circle, on the inner-node state
$PY $HP/modecount_circle.py $F/states/modecount_state_D30.0688_M48_inner015.npz 4.267,1.324,0.35 \
    2.0797477104405484,0,0.2 --fmax=1e-15 --tag=D30.0688_M48_inner015 --data=$F/inner015/data > $F/circles_inner015.log 2>&1
ex circles_inner015 $?

# 3. October's control: the same circle on October's state with a copy of October's cache
$PY $HP/modecount_circle.py $F/states/modecount_state_D30.0688_M48_october.npz 4.267,1.324,0.35 --fmax=1e-15 \
    --tag=D30.0688_M48_october --data=$F/october/data > $F/circle_october.log 2>&1
ex circle_october $?

# 4. build check: fresh determinants at two of October's cached circle points, and its control
P1=4.267,0.9740000000000001
P2=3.94364216362105,1.1900607986722187
$PY $F/scripts/fresh_vs_cache.py $HP $F/states/modecount_state_D30.0688_M48_october.npz \
    $F/october/data/modecount_D30.0688_M48_october_evals.jsonl $F/fresh_vs_cache.json $P1 $P2 > $F/fresh_vs_cache.log 2>&1
ex fresh_vs_cache $?
$PY $F/scripts/fresh_vs_cache.py $HP $F/states/modecount_state_D30.0688_M48_october.npz \
    $F/october/data/modecount_D30.0688_M48_october_evals.jsonl $F/fresh_vs_cache_mutate_swap.json $P1 $P2 --mutate=swap \
    > $F/fresh_vs_cache_mutate_swap.log 2>&1
ex fresh_vs_cache_mutate_swap $?
