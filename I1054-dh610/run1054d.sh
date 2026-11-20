#!/bin/bash
# #1043 / PR #1054, job (1) of notes/EXACT_RECIP.md 3.6 (coordinator's task of 20 Nov): --od_start_F 0 at D 246.44 and 249.47 against 3.5's flag-off bases, in main's code
# (a worktree of main at 8179068d, which holds --od_start_F) with venv-i1054's python (the build with Solver.set_exact_recip). A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054d $* $(stamp) UTC" >> $X; }
W59=/home/nathan/Source/choptuik-large-d-1059
cd $REPO || exit 1
git fetch -q origin main || exit 1
M59=$(git rev-parse 8179068d) || exit 1
git merge-base --is-ancestor 394c9f2d $M59 || { log "394c9f2d is not an ancestor of $M59: stop"; exit 1; }
[ -d $W59 ] || git worktree add -q --detach $W59 $M59 || exit 1
[ "$(git -C $W59 rev-parse HEAD)" = $M59 ] || { log "$W59 is not at $M59: stop"; exit 1; }
[ -z "$(git -C $W59 status --short)" ] || { log "worktree $W59 not clean: stop"; exit 1; }
log "worktree $W59 at $(git -C $W59 rev-parse HEAD), venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC 1054d: main $M59 in $W59; hp changes against 5f488e2b (the build of venv-i1054): $(git diff --name-only 5f488e2b $M59 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/python hp/build.sh | tr '\n' ' ')" >> $SUM
echo "# 1054d: Solver.set_exact_recip in venv-i1054: $($VENV/bin/python -c 'import hpkernel;print(hasattr(hpkernel.Solver, "set_exact_recip"), hasattr(hpkernel.Solver, "plan_auto"))' 2>&1 | tail -1) (set_exact_recip, plan_auto)" >> $SUM
for T in 246.4399 249.4664; do [ -f $OUT/resolve${T}_r0/base_pin3_D$T.npz ] || { log "the flag-off base of D $T is missing: stop"; exit 1; }; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W59/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --log_proj 1"
for S in leg01_D243.8361_ks293/anm_pin3_D246.4399 leg02_D247.2801_ks293/anm_pin3_D249.4664; do
  T=${S##*_D}
  cd $W59/hp
  { echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/resolve${T}_r1b --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip 1 --od_start_F 0"; } > $OUT/resolve${T}_r1b.log
  s0=$(date +%s); nice -n 10 timeout -s TERM 21600 python3 -u anm_run.py $RAW $OUT/resolve${T}_r1b --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip 1 --od_start_F 0 >> $OUT/resolve${T}_r1b.log 2>&1; rc=$?
  echo "exit $rc" >> $OUT/resolve${T}_r1b.log
  echo "resolve${T}_r1b: exit $rc, $(( $(date +%s) - s0 )) s (cap 21600 s); $(python3 $OUT/classify.py $OUT/resolve${T}_r1b.log)" >> $SUM; log "resolve${T}_r1b exit $rc"
  { echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1b/base_pin3_D$T.npz --out $OUT/delta${T}b.json"; } > $OUT/delta${T}b.log
  nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1b/base_pin3_D$T.npz --out $OUT/delta${T}b.json >> $OUT/delta${T}b.log 2>&1; rc=$?
  echo "exit $rc" >> $OUT/delta${T}b.log
  echo "delta${T}b: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta${T}b.log | sed 's/^ *//')" >> $SUM; log "delta${T}b exit $rc"
done
cd $OUT
python3 classify.py --selftest > classify_selftest.txt 2>&1; r1=$?; python3 classify.py --selftest --mutate > classify_selftest_mutate.txt 2>&1; r2=$?
python3 table1054.py 1b 246.4399 249.4664 > table_job1.md 2>&1
FILES="delta241.json"; for T in 246.4399 249.4664; do
  [ "$(python3 classify.py --json resolve${T}_r1b.log | python3 -c 'import json,sys;print(json.load(sys.stdin)["reading"])')" = converged ] && [ -f delta${T}b.json ] && FILES="$FILES delta${T}b.json"
done
python3 fit_change.py $FILES > fit_change_job1.txt 2>&1; rc=$?
echo "job 1: classify selftest exit $r1 (0), --mutate exit $r2 (1); fit_change.py $FILES exit $rc" >> $SUM; log "job1 summary: classify selftest $r1 mutate $r2, fit $rc"
log "job 1 done"
exit
}
