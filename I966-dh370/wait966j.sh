#!/usr/bin/env bash
# #966 (coordinator hc 2026-11-22 ~02:05 UTC): push the raw folder AT ONCE when a step has saved its series (the line 'step N: the series saved as .../jet_pin3_D<D>.npz', about 8 min after the base's acceptance),
# so that xfchecks can read the base about 10 min after it is saved. Waits until the count of those lines in the leg's log exceeds BASE, waits 5 s for the file to close, runs push966.sh, prints the push line and exits.
# usage: bash wait966j.sh LEGDIR BASE      e.g. bash wait966j.sh leg15_D263.4862_ks293 3     (BASE = the current count of 'the series saved as' lines)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
LG=ks_chain3b/$1/anm_run.log
while sleep 5; do
  n=$(grep -c '^step [0-9]*: the series saved as' $LG 2>/dev/null)
  if [ "${n:-0}" -gt "$2" ]; then
    sleep 5
    l=$(grep '^step [0-9]*: the series saved as' $LG | tail -1); f=$(echo "$l" | grep -o 'jet_pin3_D[0-9.]*\.npz')
    echo "$(date -u '+%F %T') $l" | cut -c1-200
    bash push966.sh "I966-dh370: $f saved (the series of the base), pushed at once for xfchecks" 2>&1 | tail -1
    exit 0
  fi
  [ "$(date -u +%s)" -ge "$(date -u -d '2026-11-22 04:30:00' +%s)" ] && { echo "past 04:30 UTC, no series saved"; exit 0; }
done
