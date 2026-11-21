#!/usr/bin/env bash
# #966 (coordinator's hc 2026-11-21 ~23:00 UTC): same-order restart with --h_max 0.045 (for 2) so every attempt starts at a <= 0.045: leg 14's flags (--od_accept own, --reseed_o_bar 1e-17, ks 293) plus --keep_plan 1 (driver option) --base_polish 0 --h_max 0.045; unit i966y (run966v.sh chainv), STOPUNIT default i966u, NOSTOP=1 NOSTART=1 test the dry and the gates only.
# lineage: restart966q.sh (A/B, --od_accept own) -> restart966s.sh (--reseed_o_bar 1e-17) -> this file (--keep_plan 1 --base_polish 0).
# by exact pids, then starts ks_chain3b from the highest state with chainh's flags (--tol_od 2e-34, level held at 0.00715, bar 1e-13) plus --proj_start pred
# --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1, code from -966g (perf/elim-projections 1aa4a4fb), python and hpkernel from -961 (read-only),
# ks 293 by PAD, after a --dry whose gates abort the start (run966v.sh chainv, unit i966t). NOSTOP=1 NOSTART=1 test the dry and the gates only.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
WT=/home/nathan/Source/choptuik-large-d-966g
VENV=/home/nathan/Source/choptuik-large-d-961
STOPUNIT=${STOPUNIT:-i966u}
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
if [ -z "$NOSTOP" ]; then
  bash $OUT/stop966.sh $STOPUNIT "${REASON:-add --proj_o 1 to the flags}" || { log "start966v ABORTED, the stop failed"; exit 1; }
  [ -z "$(pgrep -f 'anm_run.py|ks_chain.py' | head -1)" ] || { log "start966v ABORTED, a chain process is still running"; exit 1; }
fi
read -r D0 PAD < <(cd $WT/hp && $VENV/.venv/bin/python - <<'PY'
import glob, os, re, sys
sys.path.insert(0, os.getcwd())
import ks_chain as k
out = "/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370/ks_chain3b"
best = max((float(re.search(r"_D(\d+\.\d+)\.npz$", p).group(1)) for p in glob.glob(out + "/leg*/anm_pin*_D*.npz")))
a, b, _ = k.re_s_line()
import numpy as np
f = glob.glob(out + "/leg*/anm_pin*_D%.4f.npz" % best)[0]
z = np.load(f, allow_pickle=True)
assert all(k_ in z.files for k_ in ("zh", "zl", "z7")), f
print("%.4f" % best, 293 - k.order_for(best + 10.0, a, b, 4.4, 0))
PY
)
log "resume state D $D0, PAD $PAD"
F3=$(sed -n 's/^F3="\(.*\)"$/\1/p' $OUT/run966.sh)
F3e="${F3/--a_scale 0.0715/--a_scale 0.000715} --a_rise 1"
F3e="${F3e/--tol_od 1e-60/--tol_od 2e-34} --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1"
[[ "$F3e" == *"--h_max 2 "* ]] || { log "start966v ABORTED, F3 has no --h_max 2"; exit 1; }
F3e="${F3e/--h_max 2 /--h_max 0.045 }"
F3e="${F3e/--od_accept natural/--od_accept own} --reseed_o_bar 1e-17 --base_polish 0"
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
dry=$(cd $WT/hp && $VENV/.venv/bin/python -u ks_chain.py /home/nathan/Source/choptuik-large-d-raw-wt613 $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD --keep_plan 1 --dry -- $F3e --reseed_qd_bar 1e-13 --steps 400 2>&1)
echo "$dry" > $OUT/ks_chain3b_v_dry.log
l0=$(echo "$dry" | grep -m1 '^leg [0-9]*:')
cmd=$(echo "$dry" | grep -m1 'anm_run.py')
log "dry: $l0"
ok=1
echo "$l0" | grep -q "at ks 293 from .*anm_pin3_D$D0.npz" || ok=0
echo "$cmd" | grep -q -- "-966g/hp/anm_run.py" || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale 0.000715' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--a_rise 1 ' || ok=0
echo "$cmd" | grep -q -- '--reseed_qd_bar 1e-13' || ok=0
echo "$cmd" | grep -q -- '--a_drop' && ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od 2e-34' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--proj_start pred' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--proj_start' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_o_stop 1' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_o_stop' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_start pred' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--proj_o 1' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--proj_o' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--od_floor_delta 1e-30' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--od_floor_delta' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--ks_retry' && ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--od_accept own' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--keep_plan 1' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--h_max 0.045 ' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--h_max' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--keep_plan' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--base_polish 0' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--base_polish' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_o_bar 1e-17' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_o_bar' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--reseed_o 3 ' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--od_accept' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--od_accept natural' && ok=0
[ $ok = 1 ] || { log "start966v ABORTED, the dry run is not as expected (see ks_chain3b_v_dry.log), chain stopped"; exit 1; }
[ -n "$NOSTART" ] && { log "TEST only: dry gates ok=$ok, would start i966y (run966v.sh chainv, PAD $PAD)"; exit 0; }
log "starting i966y (run966v.sh chainv, tol_od 2e-34 + proj_start pred + reseed_o_stop 1 + od_floor_delta 1e-30 + proj_o 1, PAD $PAD)"
systemd-run --user --unit=i966y --working-directory=$OUT --setenv=PAD=$PAD systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b h_max 0.045' bash $OUT/run966v.sh chainv >> $OUT/restart966.out 2>&1
log "i966y started"
