#!/bin/bash
# #847 on rpi5 (the coordinator): Theorem A(M = 5)'s second-order certificate (proof/A_M2.md) reproduced on aarch64
# Linux, the commands of A_M2.md section 7 without the finite-difference runs (d2check reads the stored fd files) and
# the pilot. The M = 5 box run starts first in the background; the M = 1 and M = 3 paths run beside it, one process
# each. Outputs go to the raw folder, so the worktree's stored data/ files are not touched. A "ctrl" line is a control
# that must fail (exit nonzero, or its verdict line negative).
R=/home/nathan/Source/choptuik-large-d-raw/I847-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-847
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "847 $1 $(date -u '+%F %T') UTC" >> $R/exits_847.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
B1=$R/A_M2_box_M1_1e-6.json; B3=$R/A_M2_box_M3_1e-8.json; B5=$R/A_M2_box_M5_1e-10.json
run run box5 certify_M2.py box 5 --chart=data/A_M2_chart_M5.json --h=1e-10 --w=1e-18,1e-19 --out=$B5 --log=$R/A_M2_box_M5_1e-10.log &
run run  lohner_selftest      certify_M2_lohner.py selftest
run ctrl lohner_selftest_mut  certify_M2_lohner.py selftest --mutate=lin2
run run  box1                 certify_M2.py box 1 --chart=data/A_M2_chart_M1.json --h=1e-6 --w=0 --out=$B1 --log=$R/A_M2_box_M1_1e-6.log
run run  krawczyk1            certify_M2.py krawczyk --box=$B1 --shrink --reference=thmA1
run ctrl krawczyk1_mut        certify_M2.py krawczyk --box=$B1 --shrink --reference=thmA1 --mutate=ref
run run  controls1            certify_M2.py controls --box=$B1
run run  recheck1             certify_M_recheck.py $B1
run ctrl recheck1_mut         certify_M_recheck.py $B1 --mutate
run run  box3                 certify_M2.py box 3 --chart=data/A_M2_chart_M3.json --h=1e-8 --w=1e-13 --out=$B3 --log=$R/A_M2_box_M3_1e-8.log
run run  krawczyk3            certify_M2.py krawczyk --box=$B3 --shrink --reference=AM3
run run  controls3            certify_M2.py controls --box=$B3
run run  d2check3             certify_M2.py d2check --box=$B3 --fd=data/A_M2_fd_M3.json
run run  recheck3             certify_M_recheck.py $B3
run ctrl recheck3_mut         certify_M_recheck.py $B3 --mutate
run run  krawczyk5_stored     certify_M2.py krawczyk --box=data/A_M2_box_M5_1e-10.json --shrink --hier
wait
run run  krawczyk5            certify_M2.py krawczyk --box=$B5 --shrink --hier
run ctrl krawczyk5_mut        certify_M2.py krawczyk --box=$B5 --hier --mutate=hier
run run  controls5            certify_M2.py controls --box=$B5
run run  d2check5             certify_M2.py d2check --box=$B5 --fd=data/A_M2_fd_M5.json
run run  recheck5             certify_M_recheck.py $B5
run ctrl recheck5_mut         certify_M_recheck.py $B5 --mutate
log "all done"
