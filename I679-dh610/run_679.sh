#!/usr/bin/env bash
# #679: chain_dM.py planted at the kfreeze-13 plants dd40 and dd58, then the --mutate=D control, one after the other, 2 threads.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I679-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
cd /home/nathan/Source/choptuik-i679/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "cbb124b5" ] || { echo "worktree is not at cbb124b5" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for run in planted planted_mutD; do
    extra=""; [ $run = planted_mutD ] && extra="--mutate=D"
    t=$(date +%s)
    echo "$run start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_679.txt
    systemd-inhibit --what=idle:sleep --who=dh610 --why="#679 $run" \
        $PY -u chain_dM.py planted $RAW $R/$run --threads=2 --only=dd40,dd58 $extra > $R/$run.log 2>&1
    rc=$?
    echo "$run exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_679.txt
done
