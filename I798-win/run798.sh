#!/usr/bin/env bash
# #798 on win: lowD_plan_probe.py from T135's base at M 384 (T105-win2's state at D 3.04375), with T135's stored series
# (coeffs.npz copied into each output folder, so the 8 h Jacobian phase is skipped), T135's build and checkout (venv-t125,
# choptuik-t125), 6 threads, cap 900 s. First the control (--cap 0.001 at 3.0433, must exit 1 with every case capped),
# then the probe: 3.0425 (T135's planted case) and the new targets 3.0433, 3.0432, 3.0431 and 3.04305; check798.py last.
PY=/c/Users/nathan/Source/venv-t125/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw; R=$RAW/I798-win
S=T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz
cd /c/Users/nathan/Source/choptuik-t125/hp || exit 9
export OPENBLAS_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log() { echo "798 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_798.txt; }
log "start, checkout $(git rev-parse --short=8 HEAD)"
"$PY" -I $R/check798.py --selftest > $R/selftest_798.txt 2>&1; rc=$?; log "selftest exit $rc (must be 0)"; [ $rc = 0 ] || exit 1
mkdir -p $R/control $R/probe
cp $RAW/T135-win/probe/coeffs.npz $R/control/coeffs.npz
cp $RAW/T135-win/probe/coeffs.npz $R/probe/coeffs.npz
"$PY" -u lowD_plan_probe.py $RAW $R/control --state $S --targets 3.0433 --N 3 --threads 6 --cap 0.001 > $R/control.log 2>&1
log "control exit $? (must be 1, every case capped)"
"$PY" -u lowD_plan_probe.py $RAW $R/probe --state $S --targets 3.0425,3.0433,3.0432,3.0431,3.04305 --N 3 --threads 6 --cap 900 > $R/probe.log 2>&1
log "probe exit $? (1 when any case is capped)"
"$PY" -I $R/check798.py $R/probe/probe.jsonl > $R/table_798.txt 2>&1; log "check exit $? (must be 0: the planted case)"
log "all done"
