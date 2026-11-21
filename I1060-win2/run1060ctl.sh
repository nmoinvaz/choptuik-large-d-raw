#!/bin/bash
# #1060's two controls (the coordinator's hc of 2026-11-21 ~02:25 UTC), on win2 at main 8179068d, venv-i1058b, BelowNormal, one after the other:
#  1. S = 1 again, the same command as step17_s1, OUT step17_s1b; compared with step17_s1 by cmp1060.py (bits, files, close) and by the records.
#  2. series_split_check.py at anm_pin3_D260.6706.npz (ks 293) with #1034's arguments (--N 24 --threads 9 --Np 6 --split 2), absolute --out in this folder.
# Caps by the exact root pid (command line checked): 2400 s and 2700 s.
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
[ "$(git -C $W rev-parse HEAD)" = 8179068da460fe6be81312602e4c9987d17d73a3 ] && [ -z "$(git -C $W status --short)" ] || { log "worktree $W is not clean main 8179068d: stop"; exit 1; }
[ "$(git hash-object $RAWR/$STATE | cut -c1-12)" = 04e124334bf7 ] || { log "state blob hash differs: stop"; exit 1; }
echo "# $(stamp) UTC controls 1 and 2 start" >> $SUM; log "controls start"
cd $W/hp || exit 1
# ---- control 1
S=1
CMD="-u anm_run.py $RAWR $WOUT/step17_s1b $(sed "s/--series_split S/--series_split $S/" $OUT/command_line.txt)"
{ echo "# $(stamp) UTC cmd: $PY $CMD"; } > $OUT/step17_s1b.log
s0=$(date +%s)
crun step17_s1b 0 2400 anm_run.py "$PY" $CMD >> $OUT/step17_s1b.log 2>&1
echo "exit $RC" >> $OUT/step17_s1b.log
echo "step17_s1b: expected exit 0, got $RC, $(( $(date +%s) - s0 )) s wall (cap 2400 s) capped $CAPPED (control 1: S = 1 again)" >> $SUM
A=$OUT/step17_s1; B=$OUT/step17_s1b
cd $OUT
if [ -f $B/anm_pin3_D260.8483.npz ]; then
  "$PY" cmp1060.py bits $A/anm_pin3_D260.8483.npz $B/anm_pin3_D260.8483.npz > ctl1_bits.txt 2>&1; r1=$?
  "$PY" cmp1060.py files $A/jet_pin3_D260.6706.npz $B/jet_pin3_D260.6706.npz > ctl1_series.txt 2>&1; r2=$?
  "$PY" cmp1060.py files $A/pred_pin3_D260.8483.npz $B/pred_pin3_D260.8483.npz > ctl1_pred.txt 2>&1; r3=$?
  "$PY" cmp1060.py close $A/anm_pin3_D260.8483.npz $B/anm_pin3_D260.8483.npz --tol 1e-100 > ctl1_close.txt 2>&1; r4=$?
  echo "control 1: S = 1 again vs the first S = 1: state bits exit $r1 (0 = identical in all eight parts), series file exit $r2, prediction file exit $r3, close exit $r4 (ctl1_*.txt)" >> $SUM
else
  echo "control 1: no accepted state in step17_s1b: report both logs' step lines" >> $SUM
fi
"$PY" - <<'PYEOF' >> $SUM 2>&1
import json
def rec(p):
    L = [json.loads(x) for x in open(p) if x.strip()]
    r = L[-1]; at = r["attempts"][-1]
    return dict(a=at["a"], D=at["D_str"], od=at["steps"], t_coef=round(r["t_coef"], 1), t_corr=round(sum(x["t_corr"] for x in r["attempts"]), 1))
a = rec("D:/choptuik-i935-raw/I1060-win2/step17_s1/anm_run.jsonl"); b = rec("D:/choptuik-i935-raw/I1060-win2/step17_s1b/anm_run.jsonl")
print("control 1 records: first S = 1", a, "| S = 1 again", b)
PYEOF
# ---- control 2
cd $W/hp || exit 1
CMD2="-u series_split_check.py $RAWR $STATE --N 24 --threads 9 --Np 6 --split 2 --out $WOUT/split2_D260"
{ echo "# $(stamp) UTC cmd: $PY $CMD2"; } > $OUT/split2_D260.log
s0=$(date +%s)
crun split2_D260 0 2700 series_split_check.py "$PY" $CMD2 >> $OUT/split2_D260.log 2>&1
echo "exit $RC" >> $OUT/split2_D260.log
echo "split2_D260: series_split_check.py exit $RC (want 0), $(( $(date +%s) - s0 )) s wall (cap 2700 s) capped $CAPPED (control 2)" >> $SUM
log "controls done"
touch $OUT/ctl.done
touch $OUT/all.done
