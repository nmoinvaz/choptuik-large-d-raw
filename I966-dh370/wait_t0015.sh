#!/usr/bin/env bash
# #966: wakes at 2026-11-21 00:15:00 UTC, the coordinator's 3 h mark for the fallback leg's attempt 2 (report then, with the per-iteration natural ratio and the lam = 1 max|F|), or earlier on an accepted step
cap=$(date -u -d '2026-11-21 00:15:00' +%s)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
while sleep 30; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -gt 46 ] && { echo "ACCEPTED STEP before the mark: $(date -u +%R:%S)"; exit 0; }
  [ "$(date -u +%s)" -ge "$cap" ] && { echo "3 H MARK $(date -u +%R:%S): attempt 2 not converged"; exit 0; }
done
