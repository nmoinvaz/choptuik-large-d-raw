#!/bin/bash
# PR #1054 on dh610 (README.md): a worktree at the PR head, a new venv, hp/build.sh, then notes/EXACT_RECIP.md section 3: (1) the flag off against the venv-i1050 build, (2) the re-solves with --exact_recip 0 and 1,
# (3) exact_recip_check.py delta on each pair. One step at a time, nice 10, each under timeout (3 x its estimate) on its exact pid.
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; S=$OUT/summary_1054.txt
log() { echo "1054 $* $(stamp) UTC" >> $X; }
cd $REPO || exit 1
git fetch -q origin feat/exact-recip-1043 || exit 1
HEAD1054=$(git rev-parse origin/feat/exact-recip-1043)
[ -d $W ] || git worktree add -q --detach $W $HEAD1054 || exit 1
[ "$(git -C $W rev-parse HEAD)" = $HEAD1054 ] || { echo "WT is not at the branch head $HEAD1054"; exit 1; }
[ -z "$(git -C $W status --short)" ] || { echo "worktree not clean"; exit 1; }
log "start, new build at $(git -C $W rev-parse --short=8 HEAD) (origin/feat/exact-recip-1043), main build venv-i1050 (1c02b15b), load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC PR #1054 at $(git -C $W rev-parse --short=8 HEAD) against the venv-i1050 build; hp diff merge base -> head: $(git -C $W diff --stat $(git -C $W merge-base origin/main HEAD) HEAD -- hp | tail -1)" > $S
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
# runin NAME WANT CAP PYTHON-ENV-DIR cmd...: from $W/hp, log to $OUT/NAME.log, a summary line
runin() { local name=$1 want=$2 cap=$3; shift 3; cd $W/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $W/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble >> $OUT/venv.log 2>&1
echo "# python $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), lock: $(grep -A1 -E 'name = "(multidouble|multishoot|multisolver)"' $W/hp/Cargo.lock | grep -E 'name|version' | tr -d '\n' | sed 's/name = /; /g')" >> $S
runin build1054 0 5580 bash build.sh
python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), hpkernel.__file__, 'multidouble', multidouble.isa())" > $OUT/hpkernel_import.log 2>&1; echo "hpkernel import: exit $? $(tail -1 $OUT/hpkernel_import.log)" >> $S
# (1) the flag off against the venv-i1050 build: #1034's step 5 commands, compared row by row with I1050-dh610's logs (est. 1, 8, 2, 2 min; caps 30, 120, 30, 30 min)
runin step5_ref 0 1800 python3 highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
runin step5_scaled 0 7200 python3 highm_check.py scaled --compare=$RAW/T81/scaled_main.json
runin step5_jets 0 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
runin step5_jets_kappa 1 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
cd $OUT
for f in step5_ref step5_scaled step5_jets step5_jets_kappa; do
  python3 compare1050.py $OLD/$f.log $OUT/$f.log > $OUT/compare_$f.txt; r1=$?
  python3 compare1050.py $OLD/$f.log $OUT/$f.log --mutate > $OUT/compare_${f}_control.txt; r2=$?
  echo "compare $f (against I1050-dh610, the venv-i1050 build): exit $r1 (0: bit-identical rows), control --mutate exit $r2 (1): $(tail -1 $OUT/compare_$f.txt | cut -c1-200)" >> $S; log "compare $f exit $r1 control $r2"
done
# the octo-double path: exact_recip_check.py bits, saved with venv-i1050's python (main's build), compared with venv-i1054's (est. 5 min each; cap 15 min)
B=$RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz
cd $W/hp; { echo "# $(stamp) UTC cmd: $V50/bin/python exact_recip_check.py bits $B --save=$OUT/bits242_main.json --threads 10"; } > $OUT/bits242_save.log
s=$(date +%s); nice -n 10 timeout -s TERM 900 $V50/bin/python exact_recip_check.py bits $B --save=$OUT/bits242_main.json --threads 10 >> $OUT/bits242_save.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/bits242_save.log
echo "bits242_save (venv-i1050): expected exit 0, got $rc, $(( $(date +%s) - s )) s" >> $S; log "bits242_save exit $rc"
runin bits242_compare 0 900 python3 exact_recip_check.py bits $B --compare=$OUT/bits242_main.json --threads 10
runin bits242_control 1 900 python3 exact_recip_check.py bits $B --compare=$OUT/bits242_main.json --threads 10 --mutate=on
# (2) the re-solves, --exact_recip 0 and 1 (D 73: est. 5-15 min each, cap 45 min; D 241.96: 5-20 min, cap 1 h; D 251.88: 1-3 h, cap 9 h)
for R in 0 1; do
  runin resolve73_r$R 0 2700 python3 -u anm_run.py $RAW $OUT/resolve73_r$R --state T81/conv_pin5_D73.0000_D73.000000.npz --kfreeze 13 --N 24 --corrector od --tol_od 1e-60 --qd_it 12 --threads 10 --steps 0 --save_base 1 --exact_recip $R
done
for R in 0 1; do
  runin resolve241_r$R 0 3600 python3 -u anm_run.py $RAW $OUT/resolve241_r$R --state I603-win2/chain/anm_pin3_D241.9602.npz --kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 24 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 12 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --threads 10 --steps 0 --save_base 1 --exact_recip $R
done
for R in 0 1; do
  runin resolve251_r$R 0 32400 python3 -u anm_run.py $RAW $OUT/resolve251_r$R --state I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz --kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --exact_recip $R
done
# (3) Delta(exact 1/k) - Delta(recip_int) per pair (est. a minute each; cap 30 min)
runin delta241 0 1800 python3 exact_recip_check.py delta $OUT/resolve241_r0/base_pin3_D241.9602.npz $OUT/resolve241_r1/base_pin3_D241.9602.npz --out $OUT/delta241.json
runin delta251 0 1800 python3 exact_recip_check.py delta $OUT/resolve251_r0/base_pin3_D251.8782.npz $OUT/resolve251_r1/base_pin3_D251.8782.npz --out $OUT/delta251.json
runin delta73 0 1800 python3 exact_recip_check.py delta $OUT/resolve73_r0/base_pin13_D73.0000.npz $OUT/resolve73_r1/base_pin13_D73.0000.npz --out $OUT/delta73.json
log "all steps done"
