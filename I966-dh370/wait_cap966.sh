#!/usr/bin/env bash
# #966: wakes at the coordinator's cap for leg 11's base polish (2026-11-20 20:40:00 UTC), or earlier if the base polish ends ('a_rule reseed:' in any leg11_* log)
cap=$(date -u -d '2026-11-20 20:40:00' +%s)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
while sleep 20; do
  grep -qs 'a_rule reseed:' ks_chain3b/leg11_*/anm_run.log && { echo "BASE POLISH ENDED before the cap: $(date -u +%R:%S)"; exit 0; }
  [ "$(date -u +%s)" -ge "$cap" ] && { echo "CAP REACHED $(date -u +%R:%S): base polish not converged"; exit 0; }
done
