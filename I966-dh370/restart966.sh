#!/usr/bin/env bash
# #966: restart ks_chain3b at the end of the current attempt with --reseed_qd_bar 1e-15 and --pad -273 (coordinator's hc, 2026-11-19 ~00:20 UTC).
# Waits for the running attempt's 'a X -> D' line (and its 'Delta of the saved state' line, at most 30 s), then sends TERM to the exact pids of the anm_run.py
# processes of unit i966d (read from its cgroup, no name matching); ks_chain.py stops itself on the non-zero leg exit. Then starts unit i966e with run966c.sh chainc.
# Nothing else is stopped. usage: bash restart966.sh
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
cnt() { local n; n=$(grep -cE "$1" "$2" 2>/dev/null); echo ${n:-0}; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
a0=$(cnt '^ +a [0-9.]+ -> D' $LOG); v0=$(cnt 'Delta of the saved state' $LOG)
log "restart: waiting for the end of the attempt in $(basename $LEG) (a-lines $a0, saved-lines $v0)"
until [ "$(cnt '^ +a [0-9.]+ -> D' $LOG)" -gt "$a0" ]; do sleep 3; done
t1=$(date +%s)
while [ "$(cnt 'Delta of the saved state' $LOG)" -le "$v0" ] && [ $(( $(date +%s) - t1 )) -lt 30 ]; do sleep 2; done
verdict=refused; [ "$(cnt 'Delta of the saved state' $LOG)" -gt "$v0" ] && verdict=accepted
CG=/sys/fs/cgroup$(systemctl --user show i966d -p ControlGroup --value)
pids=""
for p in $(cat $CG/cgroup.procs); do
  if tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -q 'anm_run\.py .*ks_chain3b/leg'; then pids="$pids $p"; fi
done
log "the attempt ended ($verdict); TERM to the anm_run pid(s):${pids:- none}"
[ -n "$pids" ] || { log "restart ABORTED, no anm_run pid found in $CG"; exit 1; }
kill -TERM $pids
t2=$(date +%s)
until [ "$(systemctl --user is-active i966d)" != active ]; do
  [ $(( $(date +%s) - t2 )) -ge 300 ] && { log "restart ABORTED, i966d still active 5 min after the TERM"; exit 1; }
  sleep 3
done
systemctl --user reset-failed 2>/dev/null
log "i966d ended; starting i966e (run966c.sh chainc: --pad -273 --reseed_qd_bar 1e-15, same OUT)"
systemd-run --user --unit=i966e --working-directory=$OUT systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b restart' bash $OUT/run966c.sh chainc >> $OUT/restart966.out 2>&1
log "i966e started"
