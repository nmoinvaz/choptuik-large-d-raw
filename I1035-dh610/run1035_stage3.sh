#!/bin/bash
# #1035 stage 3 at D 262.0099 (dh610; the coordinator's go of 21 Nov, §5.3's commands block at ebc96296 in its order): selftests; the control first (polish293 + polishgate, step293 + stepgate; if it fails nothing is judged:
# stop); then the raise real (--tol 1e-50) and its controls real_old and real_linear (which must exit 1); polish315 + polishgate, step315 + stepgate and the delta. Each command line is diffed against §5.3's (cmddiff1035s3.py)
# before its launch, the diff kept in cmddiff_<name>.txt and the exits log, and a diff stops the launch. Caps (mine, the block has none): 14400 s per run by `timeout -s TERM` (TERM to its child). A sampler logs RSS, CPU, MemAvailable and load every
# 60 s to rss_<name>.log. GATE lines of exits_1035_stage3.txt mark the points where I post. A braced block ending in exit.
{
RAW=/home/nathan/Source/choptuik-large-d-raw; WT=/home/nathan/Source/choptuik-large-d-1035; VENV=/home/nathan/Source/venv-i1058
D=$RAW/I1035-dh610; OUT=$D/stage2; SD=$D; REF=$D/ref/section53_commands_ebc96296.txt
S3=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz; P0=I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz
RAISED=I1035-dh610/stage2/real/raise_pin3_D262.0099.npz
L14=$(sed -n 's/^L14="\(.*\)"$/\1/p' $REF)
mkdir -p $OUT
X=$OUT/exits_1035_stage3.txt; SUM=$OUT/summary_1035_stage3.txt
[ -n "$DRY1035" ] && { X=$D/dry_stage3_exits.txt; SUM=$D/dry_stage3_summary.txt; }   # DRY1035=1: only the command diffs, nothing launched
stamp() { date -u '+%F %T'; }
log() { echo "1035 s3 $* $(stamp) UTC" >> $X; }
[ "$(git -C $WT rev-parse HEAD)" = ebc96296cf779755c11adaf95bd44a0010a2750a ] || { log "worktree $WT is not at ebc96296cf779755c11adaf95bd44a0010a2750a: stop"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { log "worktree $WT not clean: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$S3 | cut -c1-8)" = eb34f3c8 ] || { log "S3's blob is not eb34f3c8: stop"; exit 1; }
[ "$(git -C $RAW hash-object --no-filters $RAW/$P0)" = 861c79ff8ffc4b10067c487287ff46286b4ed4ba ] || { log "P0's blob is not 861c79ff...: stop"; exit 1; }
[ -n "$L14" ] || { log "L14 not read from $REF: stop"; exit 1; }
log "worktree at ebc96296, venv-i1058, load $(cut -d' ' -f1-3 /proc/loadavg), S3 eb34f3c8"
. $VENV/bin/activate
cd $SD; python3 -I cmddiff1035s3.py --selftest > cmddiff1035s3_selftest.txt 2>&1; c1=$?; python3 -I cmddiff1035s3.py --selftest --break > cmddiff1035s3_selftest_break.txt 2>&1; c2=$?
echo "cmddiff1035s3.py: selftest exit $c1 (0), --break exit $c2 (1)" >> $SUM; [ $c1 = 0 ] && [ $c2 = 1 ] || { log "cmddiff controls wrong: stop"; exit 1; }
cd $WT/hp || exit 1
CAP=14400; RC=0
python3 factored_raise.py selftest $RAW/$P0 > $OUT/selftest.log 2>&1; s1=$?
python3 factored_raise.py selftest $RAW/$P0 --mutate=nopred > $OUT/selftest_nopred.log 2>&1; s2=$?
log "selftest exit $s1 (must be 0; last line: $(tail -1 $OUT/selftest.log)), nopred exit $s2 (must be 1)"
[ $s1 = 0 ] && [ $s2 = 1 ] && grep -q 'selftest: 26 of 26 pass' $OUT/selftest.log || { log "a selftest rule is not met: stop"; exit 1; }
diffgate() {  # NAME CMD-STRING [--var ...]: the diff against §5.3 before a launch; returns 0 when empty
  local N=$1 C=$2; shift 2
  python3 -I $SD/cmddiff1035s3.py --actual "$C" "$@" > $OUT/cmddiff_$N.txt 2>&1; local r=$?
  log "$N command diff against §5.3: $(tail -1 $OUT/cmddiff_$N.txt) (exit $r)"
  return $r
}
launch() {  # NAME [--var K=V ...] -- CMD...: diff, run with the sampler, record the exit
  local N=$1; shift
  local V=(); while [ "$1" != "--" ]; do V+=("$1"); shift; done; shift
  local CMD=("$@") t0=$(date +%s) peak=0 pcpu=0 line
  diffgate $N "${CMD[*]}" "${V[@]}" || { log "$N: the command differs from §5.3's: not launched"; RC=99; return; }
  [ -n "$DRY1035" ] && { RC=0; return; }
  ( "${CMD[@]}" > $OUT/$N.log 2>&1; echo $? > $OUT/$N.rc ) &
  local bg=$!
  log "$N started, subshell $bg"
  while kill -0 $bg 2>/dev/null; do
    line=$(ps -eo pid=,pcpu=,rss=,etime=,args= | grep -F "$OUT/$N " | grep -v -e grep -e timeout | grep -e 'anm_run.py' -e 'factored_raise.py' | head -1)
    if [ -n "$line" ]; then
      set -- $line; [ "$3" -gt "$peak" ] && peak=$3; pcpu=$2
      echo "$(stamp) UTC pid $1 pcpu $2 rss_kB $3 etime $4 memavail_kB $(awk '/^MemAvailable/ {print $2}' /proc/meminfo) load $(cut -d' ' -f1 /proc/loadavg)" >> $OUT/rss_$N.log
    fi
    sleep 60
  done
  wait $bg; RC=$(cat $OUT/$N.rc); local w=$(( $(date +%s) - t0 ))
  log "$N exit $RC wall ~$w s, peak sampled RSS $peak kB, last pcpu $pcpu"
  echo "$N: exit $RC, wall ~$w s (60 s samples), peak sampled RSS $peak kB, last pcpu $pcpu" >> $SUM
}
gate() {  # NAME polishgate|stepgate LOGNAME FOLDERNAME: run the gate (its command diffed too); GRC is its exit
  local N=$1 K=$2 LG=$3 FD=$4
  local CMD=(python3 factored_raise.py $K $OUT/$LG.log $OUT/$FD)
  diffgate $N "${CMD[*]}" || { log "$N: the gate command differs from §5.3's: stop"; GRC=99; return; }
  [ -n "$DRY1035" ] && { GRC=0; return; }
  "${CMD[@]}" > $OUT/$N.txt 2>&1; GRC=$?
  log "GATE $N ($K on $LG): exit $GRC: $(tail -1 $OUT/$N.txt | cut -c1-300)"
  echo "$N: exit $GRC: $(tail -1 $OUT/$N.txt | cut -c1-300)" >> $SUM
}
RAWT="timeout -s TERM $CAP nice -n 10"
# the control first, at ks 293
launch polish293 -- timeout -s TERM $CAP nice -n 10 python3 -u anm_run.py $RAW $OUT/polish293 --state $S3 $L14 --steps 0 --ks 293 --keep_plan 1 --save_base 1
gate polishgate_293 polishgate polish293 polish293; G1=$GRC
B293=I1035-dh610/stage2/polish293/base_pin3_D262.0099.npz; [ -f $RAW/$B293 ] || B293=$S3
log "B293 = $B293"
launch step293 --var B293=$B293 -- timeout -s TERM $CAP nice -n 10 python3 -u anm_run.py $RAW $OUT/step293 --state $B293 $L14 --steps 1 --ks 293 --keep_plan 1
gate stepgate_293 stepgate step293 step293; G2=$GRC
if [ $G1 != 0 ] || [ $G2 != 0 ]; then log "GATE control FAILED (polishgate $G1, stepgate $G2): nothing is judged, stop"; echo "control failed: nothing judged" >> $SUM; exit 0; fi
log "GATE control PASSED (polishgate 0, stepgate 0)"
# the raise and its controls
launch real -- timeout -s TERM $CAP nice -n 10 python3 -u factored_raise.py $RAW $OUT/real --state $S3 --ks 315 --threads 10 --tol 1e-50; R0=$RC
launch real_old -- timeout -s TERM $CAP nice -n 10 python3 -u factored_raise.py $RAW $OUT/real_old --state $S3 --ks 315 --threads 10 --tol 1e-50 --mutate=old; R1=$RC
launch real_linear -- timeout -s TERM $CAP nice -n 10 python3 -u factored_raise.py $RAW $OUT/real_linear --state $S3 --ks 315 --threads 10 --tol 1e-50 --mutate=linear; R2=$RC
log "GATE raise: real exit $R0 (must be 0), real_old exit $R1 (must be 1), real_linear exit $R2 (must be 1)"
echo "raise: real $R0 (0), real_old $R1 (1), real_linear $R2 (1)" >> $SUM
if [ $R0 != 0 ]; then log "real did not converge (exit $R0): no polish315, stop"; echo "real failed: stopped" >> $SUM; exit 0; fi
# the polish and the step at ks 315
launch polish315 -- timeout -s TERM $CAP nice -n 10 python3 -u anm_run.py $RAW $OUT/polish315 --state $RAISED $L14 --steps 0 --ks 315 --keep_plan 1 --save_base 1
gate polishgate_315 polishgate polish315 polish315; G3=$GRC
B=I1035-dh610/stage2/polish315/base_pin3_D262.0099.npz; [ -f $RAW/$B ] || B=$RAISED
log "B = $B"
launch step315 --var B=$B -- timeout -s TERM $CAP nice -n 10 python3 -u anm_run.py $RAW $OUT/step315 --state $B $L14 --steps 1 --ks 315 --keep_plan 1
gate stepgate_315 stepgate step315 step315; G4=$GRC
CMD=(python3 exact_recip_check.py delta $RAW/$S3 $RAW/$B --out $OUT/delta_315_vs_293.json)
diffgate delta "${CMD[*]}" --var B=$B && [ -z "$DRY1035" ] && { "${CMD[@]}" > $OUT/delta_315_vs_293.log 2>&1; log "delta exit $?: $(grep 'Delta(b) - Delta(a)' $OUT/delta_315_vs_293.log | sed 's/^ *//')"; }
V="PASS"; [ $G3 = 0 ] && [ $G4 = 0 ] && [ $R1 = 1 ] && [ $R2 = 1 ] || V="NOT PASS"
log "GATE stage 3 $V: polishgate $G3, stepgate $G4 at ks 315; real_old $R1, real_linear $R2"
echo "stage 3: $V (polishgate $G3, stepgate $G4 at ks 315, real_old $R1, real_linear $R2)" >> $SUM
log "done"
exit 0
}
