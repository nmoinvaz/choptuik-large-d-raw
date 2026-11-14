#!/usr/bin/env bash
# #679, the control rerun after dh610's reboot of 2026-11-13 22:52 UTC killed planted_mutD: chain_dM.py planted at dd58
# alone with --mutate=D (dd40's control had already failed as it must, -2.323e-15 against 1.1e-21), as run_679.sh
# (worktree choptuik-i679 at cbb124b5, 2 threads) with output in planted_mutD_dd58/. It must exit 1.
RAW=/home/nathan/Source/choptuik-large-d-raw
R=$RAW/I679-dh610
PY=/home/nathan/Source/choptuik-large-d/.venv/bin/python
cd /home/nathan/Source/choptuik-i679/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "cbb124b5" ] || { echo "worktree is not at cbb124b5" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
t=$(date +%s)
echo "planted_mutD_dd58 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_679.txt
systemd-inhibit --what=idle:sleep --who=dh610 --why="#679 planted_mutD_dd58" \
    nice -n 10 $PY -u chain_dM.py planted $RAW $R/planted_mutD_dd58 --threads=2 --only=dd58 --mutate=D > $R/planted_mutD_dd58.log 2>&1
rc=$?
echo "planted_mutD_dd58 exit $rc (must be 1) wall $(( $(date +%s) - t ))s $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_679.txt
exit $rc
