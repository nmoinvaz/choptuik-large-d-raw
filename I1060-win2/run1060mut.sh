#!/bin/bash
# #1060 control 2b (the coordinator's hc ~02:28 UTC): series_split_check.py --mutate 31 once, after the plain check (run1060ctl.sh's ctl.done), same arguments as control 2 plus --mutate 31, --out split2_D260_mut31.
# Must exit 1. BelowNormal (inherited), cap 2700 s by the exact root pid, alert-only watches restarted for it (they end at all.done).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1060-win2
. $OUT/lib1060.sh
V=/c/Users/nathan/Source/venv-i1058b
PY=C:/Users/nathan/Source/venv-i1058b/Scripts/python.exe
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PATH="$V/Scripts:$PATH"
RAWR=D:/choptuik-large-d-raw-push
WOUT=D:/choptuik-i935-raw/I1060-win2
W=/d/choptuik-i1060
STATE=I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.6706.npz
stamp() { date -u '+%F %T'; }
t=$(date +%s)
while [ ! -f $OUT/ctl.done ]; do
  [ $(( $(date +%s) - t )) -gt 14400 ] && { log "mut31: ctl.done not seen in 4 h, stop"; exit 1; }
  sleep 20
done
[ -f $OUT/all.done ] && mv $OUT/all.done $OUT/all.done_ctl
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/mem_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$WOUT/commit_watch.ps1" -Out "$WOUT" > /dev/null 2>&1 &
log "mut31 start"
echo "# $(stamp) UTC control 2b (--mutate 31) start" >> $SUM
cd $W/hp || exit 1
CMD2="-u series_split_check.py $RAWR $STATE --N 24 --threads 9 --Np 6 --split 2 --mutate 31 --out $WOUT/split2_D260_mut31"
{ echo "# $(stamp) UTC cmd: $PY $CMD2"; } > $OUT/split2_D260_mut31.log
s0=$(date +%s)
crun split2_D260_mut31 1 2700 series_split_check.py "$PY" $CMD2 >> $OUT/split2_D260_mut31.log 2>&1
echo "exit $RC" >> $OUT/split2_D260_mut31.log
echo "split2_D260_mut31: series_split_check.py --mutate 31 exit $RC (want 1), $(( $(date +%s) - s0 )) s wall (cap 2700 s) capped $CAPPED (control 2b)" >> $SUM
log "mut31 done"
touch $OUT/mut.done
touch $OUT/all.done
