#!/bin/bash
# #949 (coordinator's hc 2026-11-19): when dh370 pushes ks_chain3b's D 247.28 state (ks 293), read it first. Polls origin/main of the raw repository every 3 min for
# I966-dh370/ks_chain3b/*/anm_pin3_D247.2*.npz until the deadline (the 48 h stop, 2026-11-19 22:42 UTC), then runs sync949.sh and queue_new949.py (which puts a D 247.28 line first)
# and exits 0; exits 1 at the deadline without it. Relaunched 2026-11-19 06:36 UTC after the old session's watcher died with it.
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
G=/home/nathan/Source/choptuik-large-d-raw-push
DEADLINE=$(date -u -d '2026-11-19 22:42:00' +%s)
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  git -C $G fetch -q origin
  if git -C $G ls-tree -r --name-only origin/main I966-dh370/ks_chain3b | grep -q 'anm_pin3_D247\.2[0-9]*\.npz'; then
    cd $HERE && ./sync949.sh | tail -3; /home/nathan/Source/choptuik-large-d-935/.venv/bin/python queue_new949.py
    echo "seen $(date -u '+%F %T')"; exit 0
  fi
  sleep 180
done
echo "deadline reached $(date -u '+%F %T') without the D 247.28 state"; exit 1
