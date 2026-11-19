#!/usr/bin/env bash
# #966: floor-rule restart (coordinator's hc, 2026-11-19 ~15:30 UTC), run only on a trigger (leg 6's step stalls or is refused, or an accepted step's final |F| passes 1e-34):
# stops unit $STOPUNIT (default i966j) by exact pids, then starts ks_chain3b from the highest state with --tol_od 2e-34 --od_floor_delta 1e-30, code from -966f
# (octo_corrector.py, anm_run.py, od_floor_check.py of eb1002cf on 664ef3dd), python and hpkernel from -961, everything else unchanged, ks 293 by PAD, after a --dry whose gates
# abort the start (run966i.sh chaini, unit i966k). NOSTOP=1 NOSTART=1 test the dry and the gates only. -961 is not touched.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
WT=/home/nathan/Source/choptuik-large-d-966f
VENV=/home/nathan/Source/choptuik-large-d-961
STOPUNIT=${STOPUNIT:-i966j}
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
if [ -z "$NOSTOP" ]; then
  bash $OUT/stop966.sh $STOPUNIT "${REASON:-trigger of the floor rule}" || { log "start966i ABORTED, the stop failed"; exit 1; }
  [ -z "$(pgrep -f 'anm_run.py|ks_chain.py' | head -1)" ] || { log "start966i ABORTED, a chain process is still running"; exit 1; }
fi
read -r D0 PAD < <(cd $WT/hp && $VENV/.venv/bin/python - <<'PY'
import glob, os, re, sys
sys.path.insert(0, os.getcwd())
import ks_chain as k
out = "/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370/ks_chain3b"
best = max((float(re.search(r"_D(\d+\.\d+)\.npz$", p).group(1)) for p in glob.glob(out + "/leg*/anm_pin*_D*.npz")))
a, b, _ = k.re_s_line()
print(best, 293 - k.order_for(best + 10.0, a, b, 4.4, 0))
PY
)
log "resume state D $D0, PAD $PAD"
F3=$(sed -n 's/^F3="\(.*\)"$/\1/p' $OUT/run966.sh)
F3e="${F3/--a_scale 0.0715/--a_scale 0.00715} --a_rise 1"
F3e="${F3e/--tol_od 1e-60/--tol_od 2e-34} --od_floor_delta 1e-30"
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
dry=$(cd $WT/hp && $VENV/.venv/bin/python -u ks_chain.py /home/nathan/Source/choptuik-large-d-raw-wt613 $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD --dry -- $F3e --reseed_qd_bar 1e-13 --steps 400 2>&1)
echo "$dry" > $OUT/ks_chain3b_i_dry.log
l0=$(echo "$dry" | grep -m1 '^leg [0-9]*:')
cmd=$(echo "$dry" | grep -m1 'anm_run.py')
log "dry: $l0"
ok=1
echo "$l0" | grep -q "at ks 293 from .*anm_pin3_D$D0.npz" || ok=0
echo "$cmd" | grep -q -- "-966f/hp/anm_run.py" || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale 0.00715' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--a_rise 1 ' || ok=0
echo "$cmd" | grep -q -- '--reseed_qd_bar 1e-13' || ok=0
echo "$cmd" | grep -q -- '--a_drop' && ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od 2e-34' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--od_floor_delta 1e-30' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od' | wc -l)" = 1 ] || ok=0
[ $ok = 1 ] || { log "start966i ABORTED, the dry run is not as expected (see ks_chain3b_i_dry.log), chain stopped"; exit 1; }
[ -n "$NOSTART" ] && { log "TEST only: dry gates ok=$ok, would start i966k (run966i.sh chaini, PAD $PAD)"; exit 0; }
log "starting i966k (run966i.sh chaini, tol_od 2e-34 + od_floor_delta 1e-30, PAD $PAD)"
systemd-run --user --unit=i966k --working-directory=$OUT --setenv=PAD=$PAD systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b floor rule' bash $OUT/run966i.sh chaini >> $OUT/restart966.out 2>&1
log "i966k started"
