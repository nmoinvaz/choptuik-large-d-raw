#!/usr/bin/env bash
# the lines of #966's polish report from anm_run logs: the 'on k' iteration lines, chords, theta, trials, the Newton outcome, the base line, exit
# usage: bash lines966.sh LOG...
for f in "$@"; do
  echo "== $f"
  grep -E '^horizon series to order|^ +on [0-9]+( chord [0-9]+| trial lam [0-9.]+)?:|octo-double Newton|^base |projection failed|^exit|^Traceback' "$f" | cut -c1-330
done
