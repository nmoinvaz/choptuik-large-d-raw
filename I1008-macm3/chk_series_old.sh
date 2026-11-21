#!/bin/bash
# #1008 series check (the coordinator's order, 2026-11-21 about 02:25 UTC): the series at run3's first base (run2/arc_006_D259.565880.npz) formed on the
# OLD code and kernel (worktree choptuik-large-d-1008 at 9980cd93, venv-macm3-main) with run3's flags (F, ARC and --elim_switch 0 read from run_restart.sh,
# --a0 as in run3), at nice 19 beside run3, to be compared bit for bit with run3/arcjet_000_D259.565880.npz. chk_series_watch.py stops the run (exact pid)
# as soon as its arcjet is saved, before its first attempt. Usage: chk_series_old.sh [CAP_SECONDS]
CAP=${1:-14400}
MODE=chk_old
RAW=$HOME/Source/choptuik-large-d-raw-903
O=$RAW/I1008-macm3
PY=${CHK_PY:-$HOME/Source/venv-macm3-main/bin/python}
export PYTHONFAULTHANDLER=1
F=$(grep '^F=' $O/run_restart.sh | head -1 | sed 's/^F="//; s/"$//')
ARCB=$(grep '^ARC="--arclength' $O/run_restart.sh | head -1 | sed 's/^ARC="//; s/"$//')
A0=0.033899993896484376
ARC="${ARCB//\$A0/$A0} --elim_switch 0"
STATE=I1008-macm3/run2/arc_006_D259.565880.npz
cd ${CHK_CODE:-$HOME/Source/choptuik-large-d-1008}/hp || exit 9
log() { echo "1008m $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $O/exits_1008.txt; }
HK=$($PY -c "import hpkernel, multidouble, sys; print('hpkernel.__file__', hpkernel.__file__, 'isa', hpkernel.isa(), 'multidouble isa', multidouble.isa(), 'multidouble', multidouble.__file__, 'python', sys.version.split()[0])" 2>&1 | tr '\n' ' ')
if [ -n "$CHK_DRY" ]; then echo "$PY -u anm_run.py $RAW $O/$MODE --state $STATE $F --ks 135 --keep_plan 1 --steps 1 --D_max 262 $ARC"; exit 0; fi
log "$MODE start (series check at run3's first base, nice 19), code main $(git rev-parse HEAD), venv $PY: $HK; state $STATE, cap $CAP s, a0 $A0, F md5 $(printf '%s' "$F" | md5), ARC md5 $(printf '%s' "$ARC" | md5)"
t=$(date +%s)
caffeinate -is nice -n 19 $PY -u $O/capped_run.py $CAP $PY -u anm_run.py $RAW $O/$MODE --state $STATE $F --ks 135 --keep_plan 1 --steps 1 --D_max 262 $ARC > $O/$MODE.log 2>&1
rc=$?
log "$MODE exit $rc wall $(( $(date +%s) - t ))s"
exit $rc
