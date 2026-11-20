#!/usr/bin/env bash
# waits for the 'a_rule reseed:' line of leg 7's first step (the base polish's iteration lines would trip wait966c's crawl count), then hands over to wait966c.sh with the same arguments
# usage: bash wait966e.sh SEEN N LEG0
LG=ks_chain3b/leg09_D255.0004_ks293/anm_run.log
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
until grep -q 'a_rule reseed:' $LG; do
  [ "$(systemctl --user is-active i966m)" = active ] || { echo "UNIT i966m NOT ACTIVE before the first re-seed"; tail -n 4 $LG | cut -c1-200; exit 0; }
  grep -qE '^Traceback' $LG && { echo TRACEBACK; exit 0; }
  sleep 15
done
exec bash wait966c.sh "$@"
