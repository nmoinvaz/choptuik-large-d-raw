#!/bin/bash
# #889 on winb (the coordinator): Theorem A(M = 1)'s lemmas S, 6a and 6b1 on Windows x86-64, for Git Bash, with #873's
# commands (proof/A_certify.md 11.7 and 12). The stored covering is checked first (a cross-load); then the ray, and only
# after it every row recomputed with `row --j=J` (rows would skip the stored rows). Outputs go to the raw folder.
# Only the three path lines below may be changed to match the machine; nothing else.
WT=/c/Users/nathan/Source/choptuik-i889
PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
R=$RAW/I889-winb
export PYTHONUTF8=1
cd $WT/solver/proof || exit 9
[ -z "$(git status --porcelain .)" ] || { echo "STOP: the worktree's solver/proof is not clean"; exit 9; }
mkdir -p $R
log() { echo "889 $1 $(date -u '+%F %T') UTC" >> $R/exits_889.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), platform.machine(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t )) s ($kind)"
}
# lemma S, the old sector lemma and the flat estimate (11.3-11.5)
run run  sector        lemma6_sector.py --json=$R/lemma6_sector_1e-9.json
run ctrl sector_series lemma6_sector.py --mutate=series
run run  usys          lemma6_usys.py
# lemma 6a: the lower path and the backward jump (11.6); the stored box on Windows too
run run  path_point    lemma6_path.py point --out=$R/lemma6_path_point.json
run run  path_box      lemma6_path.py box --h=1e-9 --out=$R/lemma6_path_box_1e-9.json
run run  path_krawczyk lemma6_path.py krawczyk --point=$R/lemma6_path_point.json --box=$R/lemma6_path_box_1e-9.json
run run  jump          lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --json=$R/lemma6_jump_1e-9.json
run run  jump_stored   lemma6_jump.py --box=lemma6_path_box_1e-9.json --json=$R/lemma6_jump_stored_box.json
run run  jump_pi       lemma6_jump.py --box=$RAW/I873-rpi5/lemma6_path_box_1e-9.json --json=$R/lemma6_jump_pi_box.json
run ctrl jump_swap     lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --mutate=swap
run ctrl jump_coords   lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --mutate=coords
# lemma 6b1 (12): the stored covering first, then the ray, then every row recomputed, then the check
run run  disc               lemma6b1_disc.py
run run  cover_check_stored lemma6b1_cover.py check
run run  cover_ray          lemma6b1_cover.py ray
[ -s lemma6b1_runs/ray.json ] || { log "STOP: no ray.json"; exit 9; }
for j in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run run $(printf 'cover_row_%02d' $j) lemma6b1_cover.py row --j=$j
done
run run  cover_check        lemma6b1_cover.py check --json=$R/lemma6b1_check_1e-9.json
mkdir -p $R/lemma6b1_runs_winb && cp lemma6b1_runs/*.json $R/lemma6b1_runs_winb/ 2>> $R/exits_889.txt
run ctrl cover_sign         lemma6b1_cover.py --mutate=sign
run ctrl cover_drop         lemma6b1_cover.py check --drop=5,6
run ctrl cover_control      lemma6b1_cover.py control
log "all done"
