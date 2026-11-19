#!/usr/bin/env bash
# #966: stops ks_chain3b by the exact pids of ks_chain.py then its anm_run.py (read from unit $1's cgroup), keeps all logs, restarts nothing.
U=${1:?unit}
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
log() { echo "966 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_966.txt; }
CG=/sys/fs/cgroup$(systemctl --user show $U -p ControlGroup --value)
kc=""; ar=""
for p in $(cat $CG/cgroup.procs); do
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
  case "$c" in *ks_chain.py*) kc="$kc $p";; *anm_run.py*) ar="$ar $p";; esac
done
[ -n "$kc" ] && [ -n "$ar" ] || { log "stop966: pids not found in $U"; exit 1; }
log "stop966 ($U, test step 1 failed the 1e-18 bar, coordinator's rule): TERM ks_chain.py$kc then anm_run.py$ar"
kill -TERM $kc; sleep 1; kill -TERM $ar
t=$(date +%s)
until [ "$(systemctl --user is-active $U)" != active ]; do [ $(( $(date +%s) - t )) -ge 300 ] && { log "stop966: $U still active 5 min after the TERM"; exit 1; }; sleep 3; done
log "stop966: $U ended, nothing restarted"
