#!/bin/bash
# #1098 on win2 (Git Bash): fastmul7's checks on the new build (worktree /d/choptuik-i1098 at d40a9c62, venv V), each
# log and its exit code into OUT (the live raw worktree's I1098-win2/fastmul7_build/), one BLAS thread:
#   the seven #1098 checks, from hp/ with HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1:
#     relaxed_build_check (D 2000 step file), recip_check D 300 and D 1000, dmat_check D 300 and D 1000,
#     taylor_mp_check D 300, and horizon_mp_check at D 300's u h21 state, Moebius a 8 ks 1600 against mpmath (bar
#     1e-100), its control by the kernel's old split (--ctl_mutate 57, above 1e-80)
#   AGENTS.md's new-build checks against the stored references (no HP_EXACT_* set: the model's own path):
#     highm_check ref (T81, and the Windows reference T45-win as information), scaled (T81), jets (anm-mac) and
#     jets --mutate=kappa, which must fail
# Every input is a file of the raw repository, read from RAW (a clone or worktree that holds them at origin/main). The
# paths handed to Python are Windows-style (D:/...), which Git Bash passes unchanged
#
#     V=/c/Users/nathan/Source/venv-i1098 RAW=D:/choptuik-large-d-raw checks_fastmul7.sh
{
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
V=${V:-/c/Users/nathan/Source/venv-i1098}
RAW=${RAW:-D:/choptuik-large-d-raw}
OUT=${OUT:-D:/choptuik-i1098-raw-live/I1098-win2/fastmul7_build}
PY=$V/Scripts/python.exe
mkdir -p $OUT
cd /d/choptuik-i1098/hp || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
E=$OUT/exit_codes.txt
echo "# start $(date -u '+%F %T') UTC, hp $(git rev-parse --short=8 HEAD), $($PY -c 'import hpkernel; print(hpkernel.__file__, hpkernel.isa())')" >> $E
# inputs (git blob ids checked, so a missing or changed file fails here, not inside a check)
L2=$RAW/I1088-dh610/L2000/lastnode_D2000.0000_step.npz
S3=$RAW/I1098-dh610/budget300_src/D300_full_base.npz
S10=$RAW/I1098-dh610/fix/D1000_base/release_ls_h13_D1000.0000.npz
U21=$RAW/I1098-mm5/ladder/D300u/tail/release_ls_h21_D300.0000.npz
for p in "$L2 392276089bb4a24974e8359adad661a2a0bb72ba" "$S3 569779b213ca7334c01417ae53b7389863220cc9" \
         "$S10 57af5b81bf3f21bb583bbbd6773bb0a4e28a6fbc" "$U21 3f609c95495bc61f8ff0b7443fa93b2b497aae61"; do
  set -- $p
  [ "$(git hash-object --no-filters $1)" = "$2" ] || { echo "input $1: not blob $2" >> $E; exit 2; }
done
run() {  # NAME CAP_S cmd...
  local name=$1 cap=$2; shift 2
  local s=$(date +%s)
  timeout $cap "$@" > $OUT/$name.log 2>&1
  echo "$name exit=$? ($(( $(date +%s) - s )) s)" >> $E
}
(
  export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1
  run relaxed 3600 $PY -u relaxed_build_check.py $L2
  run recip300 3600 $PY -u recip_check.py $S3 --threads 4
  run recip1000 3600 $PY -u recip_check.py $S10 --threads 4
  run dmat300 3600 $PY -u dmat_check.py $S3
  run dmat1000 3600 $PY -u dmat_check.py $S10
  run taylor300 3600 $PY -u taylor_mp_check.py $S3
  run split300 10800 $PY -u horizon_mp_check.py $U21 --ks_mp 1100 --ks_mob 1600 --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80
)
J=$RAW/anm-mac/jets_inputs/jets_inputs.json
run ref_t81 1800 $PY -u highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
run ref_t45 1800 $PY -u highm_check.py ref --compare=$RAW/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80
run scaled 3600 $PY -u highm_check.py scaled --compare=$RAW/T81/scaled_main.json
run jets 1800 $PY -u highm_check.py jets --compare=$J
run jets_kappa 1800 $PY -u highm_check.py jets --compare=$J --mutate=kappa
echo "# end $(date -u '+%F %T') UTC" >> $E
touch $OUT/checks.done
exit
}
