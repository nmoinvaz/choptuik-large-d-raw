#!/bin/bash
# #949 (coordinator's hc 2026-11-19 ~03:00 UTC): when dh370 pushes ks_chain3b's D 247.28 state (ks 293), read it first. Polls origin/main of the raw repository every 3 min
# (at most 6 h) for I966-dh370/ks_chain3b/*/anm_pin3_D247.28*.npz, then runs sync949.sh and queue_new949.py (which puts a D 247.28 line first) and exits 0 (1 if not seen).
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
G=/home/nathan/Source/choptuik-large-d-raw-push
for i in $(seq 1 120); do
  git -C $G fetch -q origin
  if git -C $G ls-tree -r --name-only origin/main I966-dh370/ks_chain3b | grep -q 'anm_pin3_D247\.2[0-9]*\.npz'; then
    cd $HERE && ./sync949.sh | tail -3; /home/nathan/Source/choptuik-large-d-935/.venv/bin/python queue_new949.py
    exit 0
  fi
  sleep 180
done
exit 1
