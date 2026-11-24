#!/bin/bash
# #1082 on dh370 (t5's order, comment 7130913641 headed 12:25 UTC), one chain, unit i1082a (restarted 13:11 UTC with the memory wait lowered from 26 to 24 GB: MemAvailable was 25.25 GB, the baseline here; the first start waited for 26): after the k_c 87 leg ends and MemAvailable allows,
#  A. build hp from a new worktree of wip/qd-mode-1082 at a9975061 in a new venv (multidouble and hpkernel uninstalled first; hp/build.sh with the low-memory recipe); wall time, peak RSS, .so sha256;
#  B. bit-identity: highm_check.py ref and scaled, saved with the a2607acb build (~/Source/choptuik-large-d-1078m), compared with the new build; each compare must exit 0 and its control (a mutated reference) must exit 1;
#  C. the decisive test: mode_qd_decide.py selftest (0) and --mutate=accept_any (1), then mode_qd_decide.py OUTDIR STATE --threads=4 (exit 0 = RESOLVED).
# A stop leaves STOP_1082_<stage>.txt and 1082_DONE.txt. nice 8/10. Log: steps_1082.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1082-dh370
WT=/home/nathan/Source/choptuik-large-d-1082
WTO=/home/nathan/Source/choptuik-large-d-1078m
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
LEG=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
MS=${MS:-8,16,48,64,80,96,128}
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_1082.txt; }
stop() { echo "STOP $1: $2 ($(stamp) UTC)" > $OUT/STOP_1082_$1.txt; step "STOP $1: $2"; echo "1082 CHAIN STOPPED at $1 $(stamp) UTC" > $OUT/1082_DONE.txt; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = a9975061 ] && [ "$(blob $S96)" = 6a0f83d2 ] && [ "$(blob $WT/hp/mode_qd_decide.py)" = ffc107bf ] && [ "$(git -C $WTO rev-parse --short=8 HEAD)" = a2607acb ] || stop 0 "a worktree or the state not pinned (a9975061, a2607acb, 6a0f83d2, mode_qd_decide.py ffc107bf)"
step "waiting for the k_c 87 leg (LEG_DONE.txt, unit i1025leg87 inactive) and 24 GB of MemAvailable (#1078 build precedent: started at 25.2 GB available, peak RSS 24.29 GB, lowest MemAvailable 2.48 GB; swap 8 GB)"
end=$(( $(date +%s) + 43200 ))
while [ $(date +%s) -lt $end ]; do
  if [ -f $LEG/LEG_DONE.txt ] && [ "$(systemctl --user is-active i1025leg87)" != active ] && [ "$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" -gt 24000000 ]; then break; fi
  sleep 30
done
[ -f $LEG/LEG_DONE.txt ] || stop 0 "the leg did not end within 12 h"
# ---- A. the build
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$PATH
step "A build starts; python $(python -V 2>&1); MemAvailable $(awk '/MemAvailable/ {printf "%.1f GB", $2/1048576}' /proc/meminfo); load $(cut -d' ' -f1-3 /proc/loadavg)"
cd $WT
python -m pip uninstall -y multidouble hpkernel >> $OUT/build.log 2>&1
( echo "time,max_rss_kb,proc,mem_available_kb" > $OUT/build_samples.csv
  while sleep 15; do echo "$(date -u +%T),$(ps -eo rss=,comm= --sort=-rss | head -1 | awk '{print $1","$2}'),$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" >> $OUT/build_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 nice -n 8 bash hp/build.sh >> $OUT/build.log 2>&1; rc=$?
kill $SAMP 2>/dev/null
SO=$(ls $WT/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so 2>/dev/null | head -1)
step "A build exit $rc, wall $(( $(date +%s) - t0 )) s; peak largest-process RSS $(sort -t, -k2 -n $OUT/build_samples.csv | tail -1 | cut -d, -f2) kB; lowest MemAvailable $(sort -t, -k4 -n $OUT/build_samples.csv | sed -n 2p | cut -d, -f4) kB; $(tail -1 $OUT/build.log | cut -c1-100); .so sha256 $(sha256sum $SO | cut -c1-16)"
python -m pip list 2>/dev/null | grep -iE 'hpkernel|multidouble' >> $OUT/build_result.txt
[ $rc = 0 ] || stop A "the build exit $rc"
echo "A BUILD DONE $(stamp) UTC" > $OUT/1082_A_DONE.txt
# ---- B. bit-identity
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
PYO=$WTO/.venv/bin/python; PYN=$WT/.venv/bin/python
for K in ref scaled; do
  if [ $K = ref ]; then OPT="--Ms=$MS"; else OPT=""; fi
  t0=$(date +%s)
  ( cd $WTO/hp && nice -n 10 $PYO highm_check.py $K --save=$OUT/${K}_a2607acb.json $OPT ) > $OUT/${K}_save_a2607acb.log 2>&1; r0=$?
  step "B $K saved with the a2607acb build: exit $r0, $(( $(date +%s) - t0 )) s"
  [ $r0 = 0 ] || stop B "$K --save with the old build exit $r0"
  t0=$(date +%s)
  ( cd $WT/hp && nice -n 10 $PYN highm_check.py $K --compare=$OUT/${K}_a2607acb.json $OPT ) > $OUT/${K}_compare_new.log 2>&1; r1=$?
  step "B $K compared with the new build: exit $r1 (0 = bit for bit), $(( $(date +%s) - t0 )) s; $(tail -1 $OUT/${K}_compare_new.log | cut -c1-200)"
  if [ $K = ref ]; then   # the control: a reference with one hash changed must make the compare fail
    python3 - <<PYEOF
import json
d = json.load(open("$OUT/ref_a2607acb.json")); M = sorted(d, key=int)[0]; name = sorted(d[M])[0]
v = d[M][name]; d[M][name] = ("0" if v[0] != "0" else "1") + v[1:]
json.dump(d, open("$OUT/ref_a2607acb_mutated.json", "w"))
PYEOF
    ( cd $WT/hp && nice -n 10 $PYN highm_check.py ref --compare=$OUT/ref_a2607acb_mutated.json --Ms=8,16 ) > $OUT/ref_compare_mutated.log 2>&1; rm_=$?
    step "B ref control (one hash changed in the reference, Ms 8,16): compare exit $rm_ (1 wanted)"
    [ $rm_ = 1 ] || stop B "the ref control did not fail"
  fi
  [ $r1 = 0 ] || stop B "$K is not bit-identical with the new build (exit $r1)"
done
echo "B BIT-IDENTITY DONE $(stamp) UTC" > $OUT/1082_B_DONE.txt
# ---- C. the decisive test
cd $WT/hp
$PYN mode_qd_decide.py selftest > $OUT/decide_selftest.txt 2>&1; s0=$?
$PYN mode_qd_decide.py selftest --mutate=accept_any > $OUT/decide_selftest_mutate_accept_any.txt 2>&1; s1=$?
step "C mode_qd_decide.py selftest exit $s0 (0 wanted); --mutate=accept_any exit $s1 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] || stop C "the selftest or its control did not read as written"
t0=$(date +%s)
nice -n 10 $PYN -u mode_qd_decide.py $OUT $S96 --threads=4 > $OUT/decide.log 2>&1; rd=$?
step "C mode_qd_decide.py: exit $rd (0 = RESOLVED), $(( $(date +%s) - t0 )) s; $(tail -2 $OUT/decide.log | cut -c1-300 | tr '\n' '|')"
echo "1082 CHAIN DONE decide exit $rd $(stamp) UTC" > $OUT/1082_DONE.txt
exit 0
}
