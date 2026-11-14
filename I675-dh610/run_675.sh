#!/usr/bin/env bash
# #675: weak_corrector.py at the REF start, the frame from the LU at z0 (--split_at=start) and the old frame (--split_at=after,
# the control), one after the other, 2 threads each at nice 10. The second does not start if the first exits non-zero.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I675-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
cd /home/nathan/Source/choptuik-i675/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "0da740e1" ] || { echo "worktree is not at 0da740e1" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for s in start after; do
    t=$(date +%s)
    echo "split_$s start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_675.txt
    systemd-inhibit --what=idle:sleep --who=dh610 --why="#675 split_$s" \
        nice -n 10 $PY -u weak_corrector.py $RAW I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz \
        I461-win2/probe03125/anm_pin3_D242.5146.npz --mode=weak --k=4 --threads=2 --split_at=$s \
        --json=$R/split_$s.json > $R/split_$s.log 2>&1
    rc=$?
    echo "split_$s exit $rc wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_675.txt
    [ $rc = 0 ] || exit $rc
done
