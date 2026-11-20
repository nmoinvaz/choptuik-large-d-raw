#!/usr/bin/env bash
# leg 11 wake (ks 315, --ks_retry 3): waits for the first 'a_rule reseed:' line of ANY leg11_* dir (its base polish's iteration lines would trip wait966c's crawl count),
# wakes on a retry at a higher ks ('again at ks' in ks_chain3b_p.log), a stopped unit or a Traceback, then hands over to wait966c.sh with the same arguments
# usage: bash wait966i.sh SEEN N LEG0 UNIT      e.g. bash wait966i.sh 46 1 leg11 i966q
U=$4
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
until grep -qs 'a_rule reseed:' ks_chain3b/leg11_*/anm_run.log; do
  grep -qs 'again at ks' ks_chain3b_p.log && { echo "RETRY at a higher ks"; grep -h 'again at ks\|^leg 11' ks_chain3b_p.log | cut -c1-200; exit 0; }
  [ "$(systemctl --user is-active $U)" = active ] || { echo "UNIT $U NOT ACTIVE before the first re-seed"; tail -n 4 ks_chain3b/leg11_*/anm_run.log | cut -c1-200; exit 0; }
  grep -qsE '^Traceback' ks_chain3b/leg11_*/anm_run.log && { echo TRACEBACK; exit 0; }
  sleep 15
done
exec bash wait966c.sh "$@"
