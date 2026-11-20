#!/bin/bash
# #1043 / PR #1054, the coordinator's 21:5x UTC task: the flag-on polish with --od_start_F 0 at D 242.8630 only (leg00 anm_pin3_D242.8630, 3.6's flags), against job 2's flag-off base of the same D, in main's code
# (the worktree of main at 8179068d) with venv-i1054's python. Pass is 3.5's rule (classify.py). A braced block ending in exit.
{
. "$(dirname "$0")/common1054.sh"
X=$OUT/exits_1054.txt; SUM=$OUT/summary_1054.txt
log() { echo "1054f $* $(stamp) UTC" >> $X; }
W59=/home/nathan/Source/choptuik-large-d-1059
[ -d $W59/hp ] || { log "no $W59: stop"; exit 1; }
M59=$(git -C $W59 rev-parse HEAD); [ "$M59" = 8179068da460fe6be81312602e4c9987d17d73a3 ] || { log "$W59 is at $M59, not 8179068d: stop"; exit 1; }
[ -z "$(git -C $W59 status --short)" ] || { log "worktree $W59 not clean: stop"; exit 1; }
log "worktree $W59 at $M59, venv-i1054, load $(cut -d' ' -f1-3 /proc/loadavg)"
T=242.8630; S=leg00_D237.7132_ks291/anm_pin3_D$T
[ -f $OUT/resolve${T}_r0/base_pin3_D$T.npz ] || { log "the flag-off base of D $T is missing: stop"; exit 1; }
[ -f $RAW/I966-dh370/ks_chain3b/$S.npz ] || { log "the input state of D $T is missing: stop"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
. $VENV/bin/activate
cd $W59/hp || exit 1
F="--kfreeze 3 --held_fit data/held_fit.json --held_o 1 --N 31 --jet_o 1 --corrector od --tol_od 1e-60 --qd_it 40 --lam_stall 0.04 --od_junk 0 --reseed 2 --reseed_q 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --threads 10 --steps 0 --save_base 1 --log_proj 1"
{ echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/resolve${T}_r1b --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip 1 --od_start_F 0"; } > $OUT/resolve${T}_r1b.log
s0=$(date +%s); nice -n 10 timeout -s TERM 21600 python3 -u anm_run.py $RAW $OUT/resolve${T}_r1b --state I966-dh370/ks_chain3b/$S.npz $F --exact_recip 1 --od_start_F 0 >> $OUT/resolve${T}_r1b.log 2>&1; rc=$?
echo "exit $rc" >> $OUT/resolve${T}_r1b.log
echo "resolve${T}_r1b: exit $rc, $(( $(date +%s) - s0 )) s (cap 21600 s); $(python3 $OUT/classify.py $OUT/resolve${T}_r1b.log)" >> $SUM; log "resolve${T}_r1b exit $rc"
{ echo "# $(stamp) UTC cmd: python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1b/base_pin3_D$T.npz --out $OUT/delta${T}b.json"; } > $OUT/delta${T}b.log
nice -n 10 timeout -s TERM 1800 python3 exact_recip_check.py delta $OUT/resolve${T}_r0/base_pin3_D$T.npz $OUT/resolve${T}_r1b/base_pin3_D$T.npz --out $OUT/delta${T}b.json >> $OUT/delta${T}b.log 2>&1; rc=$?
echo "exit $rc" >> $OUT/delta${T}b.log
echo "delta${T}b: exit $rc: $(grep 'Delta(b) - Delta(a)' $OUT/delta${T}b.log | sed 's/^ *//')" >> $SUM; log "delta${T}b exit $rc"
cd $OUT
python3 table1054.py 1b $T > table_job3.md 2>&1
FILES="delta241.json"
[ "$(python3 classify.py --json resolve${T}_r1b.log | python3 -c 'import json,sys;print(json.load(sys.stdin)["reading"])')" = converged ] && [ -f delta${T}b.json ] && FILES="$FILES delta${T}b.json"
python3 fit_change.py $FILES > fit_change_job3.txt 2>&1; rc=$?
echo "job 3: table_job3.md written; fit_change.py $FILES exit $rc" >> $SUM; log "job 3 fit exit $rc"
log "job 3 done"
exit
}
