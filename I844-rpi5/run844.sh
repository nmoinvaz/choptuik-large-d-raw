#!/bin/bash
# #844 on rpi5 (the coordinator): Theorem A(M = 3)'s certificate and its M = 1 path reproduced on aarch64 Linux, the
# commands of proof/A_M.md section 8 and the first lemma checks of proof/A_lemmas_M.md, each logged with its exit code
# and wall time. Runs in the worktree ~/Source/choptuik-large-d-844 (branch wip/i844-rpi5), whose data/ and logs/ the
# m1 rerun overwrites; those files are copied into the raw folder at the end and the worktree is left as it is.
# A "must fail" control is the line marked ctrl; its exit is expected nonzero (or its verdict line negative).
R=/home/nathan/Source/choptuik-large-d-raw/I844-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-844
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "844 $1 $(date -u '+%F %T') UTC" >> $R/exits_844.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
B=$R/A_M_box_M3_1e-10.json
run run  sys_selftest        certify_M_sys.py selftest
run ctrl sys_selftest_mut    certify_M_sys.py selftest --mutate=coupling
run run  m1_rerun            certify_M.py m1 --rerun
run ctrl m1_mut              certify_M.py m1 --mutate=m1ref
run run  startcheck3         certify_M.py startcheck 3
run ctrl startcheck3_mut     certify_M.py startcheck 3 --mutate
run run  crosscheck3         certify_M.py crosscheck 3
run ctrl crosscheck3_mut     certify_M.py crosscheck 3 --mutate
run run  box3                certify_M.py box 3 --centre=data/A_M_refine_M3_c.json --use_out --h=1e-10 --w=4e-16 --out=$B --log=$R/A_M_box_M3_1e-10.log
run run  krawczyk3           certify_M.py krawczyk --box=$B --hier
run run  controls3           certify_M.py controls --box=$B
run ctrl krawczyk3_mut       certify_M.py krawczyk --box=$B --hier --mutate=hier
run run  recheck3            certify_M_recheck.py $B
run ctrl recheck3_mut        certify_M_recheck.py $B --mutate
run run  krawczyk3_stored    certify_M.py krawczyk --box=data/A_M_box_M3_1e-10.json --hier
run run  usys_M              lemma6_usys_M.py
run run  fpm_check_m1        fixed_point_M.py --check-m1
run run  fpm_M3              fixed_point_M.py --M=3
cp data/A_M_point_M1.json data/A_M_box_M1_1e-9.json logs/A_M_m1.log $R/ 2>> $R/exits_844.txt
log "all done"
