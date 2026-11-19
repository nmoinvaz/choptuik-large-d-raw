#!/usr/bin/env bash
# #966: start-only restart (coordinator's hc, 2026-11-19 ~12:20 UTC): the chain is already stopped (stop966.sh). Starts ks_chain3b again from the highest state
# that ks_chain.py can see (the D 251.2845 state is renamed bar_failed_*, so D 250.7060) with --tol_od 1.5e-35 (the bar's), --a_scale 0.00715 --a_rise 1,
# --reseed_qd_bar 1e-13, ks 293 by PAD (the order rule at D0 + 10), after a --dry whose gates abort the start (run966g.sh chaing, unit i966i).
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
WT=/home/nathan/Source/choptuik-large-d-961
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
[ -z "$(pgrep -f 'anm_run.py|ks_chain.py' | head -1)" ] || { log "start966g ABORTED, a chain process is running"; exit 1; }
[ ! -e $LEG/anm_pin3_D251.2845.npz ] || { log "start966g ABORTED, the D 251.2845 state is still visible to ks_chain.py"; exit 1; }
read -r D0 PAD < <(cd $WT/hp && $WT/.venv/bin/python - <<'PY'
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
F3e="${F3e/--tol_od 1e-60/--tol_od 1.5e-35}"
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
dry=$(cd $WT/hp && $WT/.venv/bin/python -u ks_chain.py /home/nathan/Source/choptuik-large-d-raw-wt613 $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD --dry -- $F3e --reseed_qd_bar 1e-13 --steps 400 2>&1)
echo "$dry" > $OUT/ks_chain3b_g_dry.log
l0=$(echo "$dry" | grep -m1 '^leg [0-9]*:')
cmd=$(echo "$dry" | grep -m1 'anm_run.py')
log "dry: $l0"
ok=1
echo "$l0" | grep -q "at ks 293 from .*anm_pin3_D250.7060.npz" || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale 0.00715' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--a_rise 1 ' || ok=0
echo "$cmd" | grep -q -- '--reseed_qd_bar 1e-13' || ok=0
echo "$cmd" | grep -q -- '--a_drop' && ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od 1.5e-35' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--tol_od' | wc -l)" = 1 ] || ok=0
[ $ok = 1 ] || { log "start966g ABORTED, the dry run is not as expected (see ks_chain3b_g_dry.log), chain stopped"; exit 1; }
log "starting i966i (run966g.sh chaing, tol_od 1.5e-35, PAD $PAD)"
systemd-run --user --unit=i966i --working-directory=$OUT --setenv=PAD=$PAD systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b tol_od 1.5e-35' bash $OUT/run966g.sh chaing >> $OUT/restart966.out 2>&1
log "i966i started"
