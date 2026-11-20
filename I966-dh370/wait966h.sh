#!/usr/bin/env bash
# waits for the first 'a_rule reseed:' line of a new leg (its base polish's iteration lines would trip wait966c's crawl count), then hands over to wait966c.sh with the same arguments
# usage: bash wait966h.sh SEEN N LEG0 LEGDIR UNIT      e.g. bash wait966h.sh 28 1 leg10 leg10_D255.7960_ks293 i966p
LG=ks_chain3b/$4/anm_run.log
U=$5
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
until grep -q 'a_rule reseed:' $LG 2>/dev/null; do
  [ "$(systemctl --user is-active $U)" = active ] || { echo "UNIT $U NOT ACTIVE before the first re-seed"; tail -n 4 $LG | cut -c1-200; exit 0; }
  grep -qE '^Traceback' $LG 2>/dev/null && { echo TRACEBACK; exit 0; }
  sleep 15
done
exec bash wait966c.sh "$@"
