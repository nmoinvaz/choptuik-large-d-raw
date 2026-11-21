#!/bin/bash
# #1064, the coordinator's hc of 2026-11-21 ~20:25 UTC: the same (a5) command as run1064a5.sh with the BLAS variables UNSET, as in the chain's environment (VIRTUAL_ENV, PYTHONFAULTHANDLER=1, PATH only), 4 threads, nice 10, beside the chain.
# Reading (the coordinator's, fixed before): equal to dh370's in-chain jet to 1e-40 means the BLAS thread setting is the cause; equal to my (a5) bit for bit means the cause is the in-chain state (the kept LU or the carried tangent); anything else is reported as found. dh610's controls are repeated: the blobs of the state and of the in-chain jet, the sha256 of dh610's jet, jetdiff and jetbits selftests with --break, row0check.
{
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I1064-dh370/a5_noblas
A5=$RAW/I1064-dh370/a5_restart/jet_a5_dh370.npz      # my (a5) run with the BLAS variables = 1
SD=/home/nathan/Source/choptuik-large-d-raw-push960/I1064-dh610      # dh610's scripts and jet, read only, at 94ddff79
WT=/home/nathan/Source/choptuik-large-d-966g
VENV=/home/nathan/Source/choptuik-large-d-961/.venv
S=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.7908.npz; S_BLOB=d15cb96c37f580a848328d29c2f69f4d121fc057
JREF=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D262.7908.npz; JREF_BLOB=287f4d70e93e61026bf580573c152be57090677e
JD=$SD/front_D262.7908/a5_basepolish0/jet_a5_basepolish0.npz; JD_SHA=b2322860723e03af
SUM=$OUT/summary_a5.txt; X=$OUT/exits_a5.txt
stamp() { date -u '+%F %T'; }
log() { echo "1064 a5 dh370 $* $(stamp) UTC" >> $X; }
mkdir -p $OUT
PY=$VENV/bin/python
echo "# (a5) on dh370: started $(stamp) UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" > $SUM
[ "$(git -C $RAW hash-object $RAW/$S)" = $S_BLOB ] || { log "the state's blob differs: stop"; exit 1; }
[ "$(git -C $RAW hash-object $RAW/$JREF)" = $JREF_BLOB ] || { log "the in-chain jet's blob differs: stop"; exit 1; }
[ "$(sha256sum $JD | cut -c1-16)" = $JD_SHA ] || { log "dh610's (a5) jet differs from the pushed one: stop"; exit 1; }
echo "inputs: state blob $S_BLOB, in-chain jet blob $JREF_BLOB (both equal dh610's), dh610's (a5) jet sha256 $JD_SHA (equal)" >> $SUM
$PY - >> $SUM 2>&1 <<'PYEOF'
import hpkernel
print("hpkernel.__file__", hpkernel.__file__)
print("hpkernel.isa()", hpkernel.isa())
PYEOF
echo "code: $(git -C $WT rev-parse --short=8 HEAD) in $WT; python $($PY -V 2>&1) from $VENV; the BLAS variables unset, as in the chain" >> $SUM
unset OMP_NUM_THREADS OPENBLAS_NUM_THREADS MKL_NUM_THREADS NUMEXPR_NUM_THREADS VECLIB_MAXIMUM_THREADS RAYON_NUM_THREADS
export VIRTUAL_ENV=$VENV PATH=$VENV/bin:$PATH PYTHONFAULTHANDLER=1
echo "run environment (names with OMP, BLAS, MKL, RAYON, THREAD): $(env | grep -E 'OMP|BLAS|MKL|RAYON|THREAD' | tr '\n' ' ')(empty = unset)" >> $SUM
cd $OUT
$PY -I $SD/jetdiff1064.py --selftest > jetdiff_selftest.txt 2>&1; j1=$?; $PY -I $SD/jetdiff1064.py --selftest --break > jetdiff_selftest_break.txt 2>&1; j2=$?
$PY -I $SD/jetbits1064.py --selftest > jetbits_selftest.txt 2>&1; p1=$?; $PY -I $SD/jetbits1064.py --selftest --break > jetbits_selftest_break.txt 2>&1; p2=$?
$PY -I $SD/jetdiff1064.py $RAW/$JREF $RAW/$JREF > jetdiff_ref_vs_itself.txt 2>&1; j3=$?
$PY -I $SD/row0check1064.py --selftest > row0check_selftest.txt 2>&1; r1=$?; $PY -I $SD/row0check1064.py --selftest --break > row0check_selftest_break.txt 2>&1; r2=$?
$PY -I $SD/row0check1064.py $RAW/$JREF $RAW/$S > row0check_inchain_jet.txt 2>&1; r3=$?
echo "controls: jetdiff selftest exit $j1 (0), --break exit $j2 (1), in-chain jet against itself exit $j3 (0); jetbits selftest exit $p1 (0), --break exit $p2 (1); row0check selftest exit $r1 (0), --break exit $r2 (1), in-chain jet row 0 against the stored state exit $r3 (0)" >> $SUM
[ $j1 = 0 ] && [ $j2 = 1 ] && [ $j3 = 0 ] && [ $p1 = 0 ] && [ $p2 = 1 ] && [ $r1 = 0 ] && [ $r2 = 1 ] && [ $r3 = 0 ] || { log "a control is wrong: stop"; exit 1; }
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 4 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 2 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_o_bar 1e-17 --reseed_qd_bar 1e-13 --D_max 271.1415 --base_polish 0"
mkdir -p $OUT/a5_noblas
{ echo "# $(stamp) UTC cmd: python3 -u anm_run.py $RAW $OUT/a5_noblas --state $S $F --steps 1 --ks 293 --keep_plan 1 --save_base 1"; } > $OUT/a5_noblas.log
log "starting anm_run (no BLAS variables) (4 threads, nice 10), load $(cut -d' ' -f1-3 /proc/loadavg)"
t0=$(date +%s)
( cd $WT/hp && exec nice -n 10 $PY -u anm_run.py $RAW $OUT/a5_noblas --state $S $F --steps 1 --ks 293 --keep_plan 1 --save_base 1 >> $OUT/a5_noblas.log 2>&1 )
rc=$?; t1=$(date +%s)
echo "exit $rc" >> $OUT/a5_noblas.log
J=$OUT/a5_noblas/jet_pin3_D262.7908.npz
if [ -f $J ]; then cp $J $OUT/jet_a5_noblas.npz; jh=$(sha256sum $J | cut -c1-16); else jh="no jet"; fi
echo "a5 noblas restart: exit $rc, wall $((t1 - t0)) s; jet sha256 $jh; log lines: $(grep -E 'base polish|the base keeps|series saved|Traceback|Error' $OUT/a5_noblas.log | cut -c1-200 | tr '\n' '|')" >> $SUM
log "anm_run exit $rc wall $((t1 - t0)) s jet $jh"
jd() {  # jd A B TAG
  [ -f $1 ] && [ -f $2 ] || { echo "jetdiff $3: a jet is missing" >> $SUM; return; }
  $PY -I $SD/jetdiff1064.py $1 $2 > jetdiff_$3.txt 2>&1; local rc=$?
  $PY -I $SD/jetbits1064.py $1 $2 > jetbits_$3.txt 2>&1; local rb=$?
  $PY -I $SD/jetstats1064.py $1 $2 > jetstats_$3.txt 2>&1
  echo "jetdiff $3: exit $rc: $(cat jetdiff_$3.txt); bits: exit $rb: $(cat jetbits_$3.txt)" >> $SUM; log "jetdiff $3 exit $rc bits $rb"
}
JA5=$OUT/jet_a5_noblas.npz
jd $JA5 $RAW/$JREF noblas_vs_inchain
jd $JA5 $A5 noblas_vs_a5blas1
jd $JA5 $JD noblas_vs_dh610_a5
$PY -I $SD/row0check1064.py $JA5 $RAW/$S > row0check_noblas_jet.txt 2>&1; r5=$?
echo "a5 noblas jet row 0 against the stored state: exit $r5: $(cat row0check_noblas_jet.txt)" >> $SUM; log "a5 row0 exit $r5"
log "done"; echo "a5 noblas on dh370 done" >> $SUM
exit 0
}
