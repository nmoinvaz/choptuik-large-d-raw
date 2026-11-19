#!/usr/bin/env bash
# #966: stop ks_chain3b by exact pids (ks_chain.py first, then its anm_run.py, both read from unit i966e's cgroup) and restart it with --reseed_qd_bar 1e-13
# and --pad -281 (coordinator's hc, 2026-11-19 ~03:10 UTC; the pad keeps the resumed leg at the state's ks 293, checked by --dry). Nothing else is stopped.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
cd $OUT || exit 9
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
# a running corrector would be an unfinished attempt: wait for its end line when the log's last 'a X:' line has no 'a X ->' line yet and the corrector has started
CG=/sys/fs/cgroup$(systemctl --user show i966e -p ControlGroup --value)
kc=""; ar=""
for p in $(cat $CG/cgroup.procs); do
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
  case "$c" in *ks_chain.py*) kc="$kc $p";; *anm_run.py*) ar="$ar $p";; esac
done
log "restart 03d: ks_chain.py pid(s)$kc, anm_run.py pid(s)$ar; last state $(ls $LEG/anm_pin3_D*.npz | tail -1 | xargs basename)"
[ -n "$kc" ] && [ -n "$ar" ] || { log "restart ABORTED, pids not found"; exit 1; }
kill -TERM $kc; sleep 1; kill -TERM $ar
t2=$(date +%s)
until [ "$(systemctl --user is-active i966e)" != active ]; do
  [ $(( $(date +%s) - t2 )) -ge 300 ] && { log "restart ABORTED, i966e still active 5 min after the TERM"; exit 1; }
  sleep 3
done
systemctl --user reset-failed 2>/dev/null
log "i966e ended; starting i966f (run966d.sh chaind: --pad -281 --reseed_qd_bar 1e-13, same OUT)"
systemd-run --user --unit=i966f --working-directory=$OUT systemd-inhibit --what=idle:sleep --who=dh370 --why='#966 ks_chain3b restart 2' bash $OUT/run966d.sh chaind >> $OUT/restart966.out 2>&1
log "i966f started"
