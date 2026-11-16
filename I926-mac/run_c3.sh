#!/bin/bash
# #926 criterion 3 at small M: one lowD_highM.py point (D 4 -> 3.99, M 48 / 64, from I95-mac's states) without and
# with --sonic_refine 4 --sonic_stop; the pair's Delta must agree to 1e-12 (bit for bit expected: the options act
# only on a nan start or near x = c, and at D 4 no node has c - x below 1e-2).
# Run from hp/ of the choptuik-large-d checkout at branch wip/sa-926; RAW is the raw-data clone (or worktree) root.
set -u
PY=${PY:-python3}
RAW=${RAW:-../../choptuik-large-d-raw}
R=$RAW/I926-mac
for v in plain sonic; do
    mkdir -p $R/c3_$v
    extra=""
    [ $v = sonic ] && extra="--sonic_refine 4 --sonic_stop"
    nice -n 10 $PY -u lowD_highM.py --start_w $RAW/I95-mac/states/lowDn_D4.0000_M48.npz \
        --start_n $RAW/I95-mac/states/lowDn_D4.0000_M64.npz --Ms 48,64 --dD 0.01 --D_end 3.985 --diff_max 1e-5 \
        --threads 4 --tag c3$v --states $R/c3_$v/states --out $R/c3_$v/leg.jsonl --points $R/c3_$v/points.jsonl \
        $extra > $R/c3_$v/leg.log 2>&1
    echo "c3 $v exit $?" >> $R/c3_exits.txt
done
