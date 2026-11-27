#!/bin/bash
# #1098 on win2 (the coordinator's hc of 2026-11-26 21:50 UTC): the standing Moebius check, added to step 3 after checks_fastmul7.sh and before D 3214 (about 35 min):
# horizon_mp_check.py of wip/large-d-form-s at 5b31dedf as hp/horizon_mp_check_v2.py, on the D300u h21 state (raw I1098-mm5/ladder/D300u/tail/release_ls_h21_D300.0000.npz, blob 3f609c95, read from the
# full checkout D:/choptuik-large-d-raw-743p), --ks_mp 1100 --ks_mob 800 --mp_mob 1 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80, HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1, one BLAS thread.
# Expected: exit 0; arithmetic 9.744e-129 (bar 1e-100); truncation 4.647e-70 (does not gate); controls 4.62e-28 and 1.7e-60. A failure is a stop.
# Waits for fastmul7_build/checks.done (checks_fastmul7.sh's last act); runs nothing if the build did not exit 0 or checks.done never comes (STOP). The result line goes to exit_codes.txt as the order says.
# usage: split_mpmob.sh   (DRY=1: the pins and the commands only)
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i1098-raw-live/I1098-win2/fastmul7_build; WOUT=D:/choptuik-i1098-raw-live/I1098-win2/fastmul7_build
WT=/d/choptuik-i1098
V=/c/Users/nathan/Source/venv-i1098; PY=$V/Scripts/python.exe
STATE=D:/choptuik-large-d-raw-743p/I1098-mm5/ladder/D300u/tail/release_ls_h21_D300.0000.npz
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a $OUT/split_mpmob_events.txt; }
git -C $WT fetch -q origin wip/large-d-form-s 2>&1 | tail -1
[ "$(git -C $WT rev-parse 5b31dedf:hp/horizon_mp_check.py | cut -c1-8)" = 131ff6e7 ] || { say "STOP: horizon_mp_check.py at 5b31dedf is not blob 131ff6e7"; exit 2; }
[ "$(git hash-object --no-filters $STATE | cut -c1-8)" = 3f609c95 ] || { say "STOP: the D300u h21 state is not blob 3f609c95"; exit 2; }
say "pins ok (horizon_mp_check.py at 5b31dedf blob 131ff6e7; D300u h21 state blob 3f609c95)"
[ "${DRY:-0}" = 1 ] && { say "DRY: waits for checks.done, then horizon_mp_check_v2.py $STATE --ks_mp 1100 --ks_mob 800 --mp_mob 1 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80"; exit 0; }
until [ -e $OUT/checks.done ] || [ -e $OUT/build_refused.txt ]; do sleep 30; done
[ -e $OUT/checks.done ] || { say "STOP: the build or its checks did not finish (no checks.done): the Moebius check does not run"; exit 3; }
say "checks.done is there; the Moebius check starts"
git -C $WT show 5b31dedf:hp/horizon_mp_check.py > $WT/hp/horizon_mp_check_v2.py
say "hp/horizon_mp_check_v2.py written, blob $(git hash-object --no-filters $WT/hp/horizon_mp_check_v2.py | cut -c1-8)"
cd $WT/hp || exit 1
s0=$(date +%s)
HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 $PY -u horizon_mp_check_v2.py $STATE --ks_mp 1100 --ks_mob 800 --mp_mob 1 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80 > $WOUT/split300_mpmob.log 2>&1
rc=$?
echo "split mpmob exit=$rc" >> $WOUT/exit_codes.txt
say "split300_mpmob exit $rc after $(( $(date +%s) - s0 )) s"
touch $OUT/split_mpmob.done
exit 0
