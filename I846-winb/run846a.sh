#!/bin/bash
# stage 1 of #846 (runner's launcher; runs the issue's commands as given, one at a time)
W=/c/Users/nathan/Source/choptuik-i846
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
O=$RAW/I846-winb
PY=/c/Users/nathan/Source/venv-t179/Scripts/python.exe
export OPENBLAS_NUM_THREADS=4
cd "$W" || exit 99
ts() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
step() { n=$1; shift; echo "$n start $(ts)" >> "$O/exits_846.txt"; "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$n exit $rc $(ts)" >> "$O/exits_846.txt"; }
step selftest        $PY matter/sigma_ms/to_sigdss.py --selftest
step selftest_shift  $PY matter/sigma_ms/to_sigdss.py --selftest --mutate=shift
step selftest_parity $PY matter/sigma_ms/to_sigdss.py --selftest --mutate=parity
for DK in "9 15" "9 23" "10 15" "10 23"; do
  set -- $DK; D=$1; kc=$2
  step seed_D${D}_kc${kc} $PY matter/sigma_ms/to_sigdss.py $RAW/I652-mac/out/sm_eta1_D${D}_M32.npz $O/seed_D${D}_kc${kc}.npy --kc $kc --D $D --eps 1
done
echo "stage1 all done $(ts)" >> "$O/exits_846.txt"
