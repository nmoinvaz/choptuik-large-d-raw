#!/bin/bash
# I1060-dh170: dh610's run1060b.sh with PATHS and the 3 h cap only changed (RAW is the state root ~/scratch1060/raw, OUT this folder, W and VENV the main 8179068d build of #1058 on dh170; the cap by exact pid under /usr/bin/time -v instead of timeout). dh610's header follows.
# #1060b (coordinator's task of 21 Nov, after #1064): step 1's command with --base_polish 0 added, OUT step17_s1_nobp (the stored state is the base, no polish), compared by cmp1060.py with leg 10's stored D 260.8483 state as in step 1; reading fixed by the coordinator:
# equal bits (Delta and the exactly summed parts): the 1.188e-20 came from the base polish; unequal with the base unmoved: the build (1aa4a4fb python on a 40f4b4a5 kernel against 8179068d) or the platform. The text below is step 1's run1060.sh with the names changed.
# #1060 on dh610, after #1043 job 6: leg 10's step 17 (D 260.6706 -> 260.8483, a 0.1777) of dh370's ks_chain3b run again on venv-i1058 (main 8179068d, worktree -1060), with leg 10's own anm_run command line
# (the dry log I966-dh370/ks_chain3b_m_dry.log, run966m.sh chainm: F3m + --reseed_qd_bar 1e-13 --steps 400 --ks 293 --keep_plan 0 --D_max 266.1776) with --steps 1, --D_max 300 and an absolute OUT.
# Amended by the coordinator (hc, 21 Nov, twice): only step 1, leg 10's line exactly as it ran (--series_split 1), which must equal the stored state bit for bit, judged on Delta and the exactly summed
# parts (cmp1060.py bits), the per-part bytes and M1 as information; the split-2 A/B is win2's. A braced block ending in exit.
{
RAW=/home/nathan/scratch1060/raw; OUT=/home/nathan/Source/choptuik-large-d-raw/I1060-dh170
W=/home/nathan/Source/choptuik-large-d-1058b; VENV=/home/nathan/Source/choptuik-large-d-1058b/.venv
X=$OUT/exits_1060b.txt; SUM=$OUT/summary_1060b.txt
stamp() { date -u '+%F %T'; }
log() { echo "1060b $* $(stamp) UTC" >> $X; }
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
[ "$(git -C $W rev-parse HEAD)" = 8179068da460fe6be81312602e4c9987d17d73a3 ] && [ -z "$(git -C $W status --short)" ] || { log "worktree $W is not clean main 8179068d: stop"; exit 1; }
REFD=$RAW/I966-dh370/ks_chain3b/leg10_D256.1776_ks293
for f in anm_pin3_D260.6706.npz anm_pin3_D260.8483.npz jet_pin3_D260.6706.npz pred_pin3_D260.8483.npz anm_run.jsonl; do [ -f $REFD/$f ] || { log "missing $REFD/$f: stop"; exit 1; }; done
. $VENV/bin/activate
echo "# $(stamp) UTC 1060: venv-i1058 hpkernel $(python -c 'import hpkernel;print(hpkernel.__file__, hasattr(hpkernel.Solver,"set_exact_recip"))' 2>&1 | tail -1); worktree $W at $(git -C $W rev-parse --short HEAD); load $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
log "start, load $(cut -d' ' -f1-3 /proc/loadavg)"
mkdir -p $OUT/ctl_b; cd $OUT/ctl_b
# the comparator's controls first (the script stops when one is wrong)
c=0
python3 $OUT/cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $REFD/anm_pin3_D260.8483.npz > ctl_bits.txt 2>&1; [ $? = 0 ] || c=1
python3 $OUT/cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $REFD/anm_pin3_D260.8483.npz --mutate > ctl_bits_mutate.txt 2>&1; [ $? = 1 ] || c=1
python3 $OUT/cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $REFD/anm_pin3_D260.8483.npz --mutate z7 > ctl_bits_mutate_z7.txt 2>&1; [ $? = 1 ] || c=1
python3 $OUT/cmp1060.py files $REFD/jet_pin3_D260.6706.npz $REFD/jet_pin3_D260.6706.npz --mutate > ctl_files_mutate.txt 2>&1; [ $? = 1 ] || c=1
for E in 1e-120 1e-90; do python3 $OUT/cmp1060.py plant $E $REFD/anm_pin3_D260.8483.npz $OUT/ctl_b/planted_$E.npz > ctl_plant_$E.txt 2>&1; python3 $OUT/cmp1060.py close $REFD/anm_pin3_D260.8483.npz $OUT/ctl_b/planted_$E.npz > ctl_close_$E.txt 2>&1; r=$?; [ $E = 1e-120 ] && [ $r != 0 ] && c=1; [ $E = 1e-90 ] && [ $r != 1 ] && c=1; done
python3 $OUT/cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $OUT/ctl_b/planted_1e-120.npz > ctl_bits_planted.txt 2>&1; [ $? = 1 ] || c=1
echo "comparator controls: $([ $c = 0 ] && echo 'all as required' || echo WRONG) (ctl_b/ctl_*.txt)" >> $SUM; log "comparator controls c=$c"
[ $c = 0 ] || exit 1
cd $W/hp || exit 1
for S in 1; do
  cd $W/hp
  CMD="python3 -u anm_run.py $RAW $OUT/step17_s${S}_nobp --state I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.6706.npz --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.00715 --jet_tangent_from 1 --series_split $S --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 1 --ks 293 --keep_plan 0 --D_max 300 --base_polish 0"
  { echo "# $(stamp) UTC cmd: $CMD"; } > $OUT/step17_s${S}_nobp.log
  s0=$(date +%s)
  nice -n 10 /usr/bin/time -v $CMD >> $OUT/step17_s${S}_nobp.log 2>&1 &
  tp=$!; echo $tp > $OUT/time_pid.txt; log "anm_run started under /usr/bin/time pid $tp (python child follows)"
  while kill -0 $tp 2>/dev/null; do                       # the 3 h cap, by exact pid (the python child and its time parent), no pattern
    if [ $(( $(date +%s) - s0 )) -gt 10800 ]; then
      py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); log "3 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
    fi
    sleep 10
  done
  wait $tp; rc=$?
  echo "exit $rc" >> $OUT/step17_s${S}_nobp.log
  echo "step17_s${S}_nobp: exit $rc, $(( $(date +%s) - s0 )) s wall (cap 10800 s)" >> $SUM; log "step17_s${S}_nobp exit $rc"
  N=$OUT/step17_s${S}_nobp/anm_pin3_D260.8483.npz
  if [ ! -f $N ]; then echo "step17_s${S}_nobp: no state anm_pin3_D260.8483.npz in the output: D differs (or the step failed); reading: report both logs' step lines and stop" >> $SUM; log "s$S: no state at D 260.8483, stop"; cd $OUT; python3 report1060b.py > report_1060b.md 2>&1; exit 0; fi
  python3 $OUT/cmp1060.py bits $REFD/anm_pin3_D260.8483.npz $N > $OUT/cmp_s${S}_nobp_vs_leg10.txt 2>&1
  if grep -q "D_str equal False\|a equal False" $OUT/cmp_s${S}_nobp_vs_leg10.txt; then echo "step17_s${S}_nobp: a or D differ from leg 10's step 17 ($(head -1 $OUT/cmp_s${S}_nobp_vs_leg10.txt | cut -c1-200)); reading: report both logs' step lines and stop" >> $SUM; log "s$S: a or D differ, stop"; cd $OUT; python3 report1060b.py > report_1060b.md 2>&1; exit 0; fi
done
cd $OUT
python3 report1060b.py > report_1060b.md 2>&1
echo "job 1060: report_1060b.md written" >> $SUM; log "1060b done"
exit
}
