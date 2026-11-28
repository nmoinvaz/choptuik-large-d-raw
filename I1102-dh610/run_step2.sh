#!/bin/bash
# #1102 step 2: build ellrs into venv-i1058, then the four gates (selftest, nolam, harm, k_c 31 check). Stops at the first
# outcome that is not the wanted one. Run as a systemd user unit.
RAW=/home/nathan/Source/choptuik-large-d-raw-1102/I1102-dh610
IN=/home/nathan/scratch1102/in
export VIRTUAL_ENV=/home/nathan/Source/venv-i1058
export PATH=$VIRTUAL_ENV/bin:$HOME/.cargo/bin:$PATH
cd /home/nathan/Source/choptuik-ell1fast/solver/matter || exit 9
say() { echo "$* $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/exits_1102.txt; }
say "build start"
CARGO_BUILD_JOBS=6 ellrs/build.sh > $RAW/build.log 2>&1
rc=$?; say "build exit $rc"; [ $rc -eq 0 ] || exit 1
export OPENBLAS_NUM_THREADS=1
python ell_b12rs.py selftest > $RAW/selftest.log 2>&1;               rc=$?; say "selftest exit $rc (want 0)";        [ $rc -eq 0 ] || exit 1
python ell_b12rs.py selftest --mutate=nolam > $RAW/selftest_nolam.log 2>&1; rc=$?; say "selftest nolam exit $rc (want 1)"; [ $rc -eq 1 ] || exit 1
python ell_b12rs.py selftest --mutate=harm > $RAW/selftest_harm.log 2>&1;   rc=$?; say "selftest harm exit $rc (want 1)";  [ $rc -eq 1 ] || exit 1
python ell_b12rs.py check $IN/l1kc31r1025.jsonl $IN/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1 > $RAW/check.log 2>&1
rc=$?; say "check exit $rc (want 0)"; [ $rc -eq 0 ] || exit 1
say "step 2 done"
