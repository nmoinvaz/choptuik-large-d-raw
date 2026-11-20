#!/bin/bash
# PR #1054, D 251.88 flag-on polish with --od_start_F 0 (coordinator's task of 20 Nov 17:4x UTC): the worktree to 4204c9f9 (only hp/anm_run.py, hp/arclength.py, hp/exact_recip_check.py and the note changed since the
# 5f488e2b build, so venv-i1054 stands), the run with --od_start_F 0 --log_proj 1, the pass rule (check251b.py), then exact_recip_check.py delta against the flag-off base of resolve251_r0.
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; S=$OUT/summary_1054.txt
log() { echo "1054b $* $(stamp) UTC" >> $X; }
cd $W || exit 1
[ -z "$(git status --short)" ] || { echo "worktree not clean"; exit 1; }
git fetch -q origin feat/exact-recip-1043 || exit 1
echo "# $(stamp) UTC 1054b: HEAD before the checkout $(git rev-parse HEAD)" >> $S
git checkout -q --detach 4204c9f9 || exit 1
HB=$(git rev-parse HEAD); log "git rev-parse HEAD $HB (feat/exact-recip-1043 at the checkout: $(git rev-parse --short=8 origin/feat/exact-recip-1043)), load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC 1054b: HEAD $HB; changed since 5f488e2b: $(git diff --name-only 5f488e2b HEAD | tr '\n' ' '); hp/src changes: $(git diff --stat 5f488e2b HEAD -- hp/src hp/Cargo.toml hp/Cargo.lock | wc -l) lines (must be 0)" >> $S
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W/hp || exit 1
CMD="python3 -u anm_run.py $RAW $OUT/resolve251_r1b --state I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz --kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --exact_recip 1 --od_start_F 0 --log_proj 1"
{ echo "# $(stamp) UTC cmd: $CMD"; } > $OUT/resolve251_r1b.log
s=$(date +%s); nice -n 10 timeout -s TERM 32400 $CMD >> $OUT/resolve251_r1b.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/resolve251_r1b.log
echo "resolve251_r1b: expected exit 0, got $rc, $(( $(date +%s) - s )) s (cap 32400 s) $([ $rc = 0 ] && echo OK || echo MISMATCH)" >> $S; log "resolve251_r1b exit $rc (expected 0)"
cd $OUT; python3 check251b.py resolve251_r1b.log > check251b.txt 2>&1; rc=$?
echo "check251b (the coordinator's pass rule) on resolve251_r1b.log: exit $rc: $(tail -1 check251b.txt); controls: resolve251_r0.log $(python3 check251b.py resolve251_r0.log >/dev/null 2>&1 && echo PASS || echo FAIL) (expected PASS), resolve251_r1.log $(python3 check251b.py resolve251_r1.log >/dev/null 2>&1 && echo PASS || echo FAIL) (expected FAIL)" >> $S; log "check251b exit $rc"
cd $W/hp
{ echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/resolve251_r0/base_pin3_D251.8782.npz $OUT/resolve251_r1b/base_pin3_D251.8782.npz --out $OUT/delta251b.json"; } > $OUT/delta251b.log
s=$(date +%s); nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/resolve251_r0/base_pin3_D251.8782.npz $OUT/resolve251_r1b/base_pin3_D251.8782.npz --out $OUT/delta251b.json >> $OUT/delta251b.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/delta251b.log
echo "delta251b: expected exit 0, got $rc, $(( $(date +%s) - s )) s $([ $rc = 0 ] && echo OK || echo "MISMATCH (see the log: no flag-on base if the rule failed)")" >> $S; log "delta251b exit $rc"
log "all steps done"
