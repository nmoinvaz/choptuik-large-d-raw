#!/bin/bash
# #912: lemma S's series control over a box (#865's fix, main 26eb48e9) on another platform, against the Mac's
# I865-mac. Usage: bash run912.sh PY RAWROOT WT MACHINE  (venv python, raw clone root, worktree at main 40cbc871 or later,
# rpi5 or winb). Each line of exits.txt has the run, its exit status, the status it must have, and its wall time.
PY=$1; ROOT=$2; WT=$3; MACH=$4
export PYTHONUTF8=1
R=$ROOT/I912-$MACH
cd $WT/solver/proof || exit 9
git merge-base --is-ancestor 26eb48e9 HEAD || { echo "STOP: the worktree is older than 26eb48e9"; exit 9; }
mkdir -p $R
{ echo "commit $(git rev-parse --short=8 HEAD)"; $PY -c "import flint, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, platform.platform(), 'python', sys.version.split()[0])"; } > $R/env.txt 2>&1
: > $R/exits.txt
run() {  # name, required exit, then the arguments
  local name=$1 want=$2; shift 2
  local t=$(date +%s)
  $PY -u "$@" > $R/$name.log 2>&1
  echo "$name: exit $? (must be $want), $(( $(date +%s) - t )) s" >> $R/exits.txt
}
run s3 0 lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --json=$R/s3.json
run s5 0 lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --Z=0.004489 --json=$R/s5.json
run s1 0 lemma6_sector.py --box=1e-9
run m3box 0 lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --mutate=series
run m5box 0 lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --mutate=series
run m5box9 0 lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-9 --mutate=series
run m1box 0 lemma6_sector.py --box=1e-9 --mutate=series
# the control: the code before the fix must not catch the box mutation (exit 3)
git show 34b00905:solver/proof/lemma6_sector_M.py > lemma6_sector_M_prefix.py
run m3box_prefix 3 lemma6_sector_M_prefix.py --M=3 --rp=0.1 --k=20 --box=1e-6 --mutate=series
rm -f lemma6_sector_M_prefix.py
for f in s3 s5; do cmp -s $R/$f.json $ROOT/I865-mac/$f.json && echo "$f.json equals the Mac's" || echo "$f.json DIFFERS from the Mac's"; done >> $R/exits.txt
echo done >> $R/exits.txt
