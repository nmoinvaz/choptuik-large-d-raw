#!/usr/bin/env bash
# #966: lever restart v2 (coordinator's hc, 2026-11-19 ~09:3x UTC): as restart966c.sh, plus a cap: if the running attempt has not ended by
# DEADLINE (epoch s, default 2026-11-19 10:00:00 UTC, the attempt's 3 h mark) the chain is stopped then, in its corrector, and restarted at once.
# A0/V0 (env) are the a-line and saved-line counts when restart966c.sh began waiting. evid966.sh copies the attempt's lines before the TERM.
# (v1: stop ks_chain3b at the end of the running attempt (no corrector is cut), by exact pids
# (ks_chain.py, then its anm_run.py, read from unit i966f's cgroup), then restart from the highest state with --a_scale 0.00715 --a_rise 1 and the same other flags
# (run966e.sh chaine). PAD is computed so that the resumed leg keeps ks 293 (the order rule at the leg's end D0 + 10), and checked with --dry. Nothing else is stopped.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
WT=/home/nathan/Source/choptuik-large-d-961
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
a0=${A0:-$(cnt '^ +a [0-9.]+ -> D' $LOG)}; v0=${V0:-$(cnt 'Delta of the saved state' $LOG)}
DL=${DEADLINE:-$(date -u -d '2026-11-19 10:00:00' +%s)}
log "lever restart v2: waiting for the end of the attempt in $(basename $LEG) (a-lines $a0, saved-lines $v0) or the cap at $(date -u -d @$DL '+%H:%M:%S UTC')"
until [ "$(cnt '^ +a [0-9.]+ -> D' $LOG)" -gt "$a0" ] || [ "$(date +%s)" -ge "$DL" ]; do sleep 3; done
if [ "$(cnt '^ +a [0-9.]+ -> D' $LOG)" -gt "$a0" ]; then
  t1=$(date +%s)
  while [ "$(cnt 'Delta of the saved state' $LOG)" -le "$v0" ] && [ $(( $(date +%s) - t1 )) -lt 30 ]; do sleep 2; done
  verdict=refused; [ "$(cnt 'Delta of the saved state' $LOG)" -gt "$v0" ] && verdict=accepted
else
  verdict="not ended, cut at the 3 h cap"
fi
bash $OUT/evid966.sh _at_stop >> $OUT/restart966.out 2>&1
CG=/sys/fs/cgroup$(systemctl --user show i966f -p ControlGroup --value)
kc=""; ar=""
for p in $(cat $CG/cgroup.procs); do
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
  case "$c" in *ks_chain.py*) kc="$kc $p";; *anm_run.py*) ar="$ar $p";; esac
done
log "the attempt: $verdict; ks_chain.py pid(s)$kc, anm_run.py pid(s)$ar"
[ -n "$kc" ] && [ -n "$ar" ] || { log "lever restart ABORTED, pids not found"; exit 1; }
[ -n "$TESTONLY" ] && { log "TEST only: would TERM $kc then $ar, nothing stopped"; exit 0; }
kill -TERM $kc; sleep 1; kill -TERM $ar
t2=$(date +%s)
until [ "$(systemctl --user is-active i966f)" != active ]; do
  [ $(( $(date +%s) - t2 )) -ge 300 ] && { log "lever restart ABORTED, i966f still active 5 min after the TERM"; exit 1; }
  sleep 3
done
systemctl --user reset-failed 2>/dev/null
# the resume state and the pad that keeps its order
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
BASE=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz
dry=$(cd $WT/hp && $WT/.venv/bin/python -u ks_chain.py /home/nathan/Source/choptuik-large-d-raw-wt613 $OUT/ks_chain3b --state $BASE --D_stop 400 --mult 4.4 --pad $PAD --dry -- $F3e --reseed_qd_bar 1e-13 --steps 400 2>&1)
echo "$dry" > $OUT/ks_chain3b_e_dry.log
l0=$(echo "$dry" | grep -m1 '^leg [0-9]*:')
cmd=$(echo "$dry" | grep -m1 'anm_run.py')
log "dry: $l0"
ok=1
echo "$l0" | grep -q "at ks 293 from" || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale 0.00715' | wc -l)" = 1 ] || ok=0
[ "$(echo "$cmd" | grep -o -- '--a_scale' | wc -l)" = 1 ] || ok=0
echo "$cmd" | grep -q -- '--a_rise 1 ' || ok=0
echo "$cmd" | grep -q -- '--reseed_qd_bar 1e-13' || ok=0
echo "$cmd" | grep -q -- '--a_drop' && ok=0
[ $ok = 1 ] || { log "lever restart ABORTED, the dry run is not as expected (see ks_chain3b_e_dry.log), chain stopped"; exit 1; }
log "i966f ended; starting i966g (run966e.sh chaine, PAD $PAD)"
systemd-run --user --unit=i966g --working-directory=$OUT --setenv=PAD=$PAD systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b lever' bash $OUT/run966e.sh chaine >> $OUT/restart966.out 2>&1
log "i966g started"
