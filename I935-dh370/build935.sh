#!/bin/bash
# #935 on dh370: hp/build.sh against multidouble 4.8.2, low-memory recipe, 10 jobs at nice 15.
# Samples the system's used and available memory (MB) every 30 s into mem.log beside it.
R=/home/nathan/Source/choptuik-large-d-raw-wt613/I935-dh370
W=/home/nathan/Source/choptuik-large-d-935
cd "$W" || exit 1
echo "start $(date -u '+%F %T') $(git log -1 --format=%h)" >> "$R/exits_935.txt"
( while true; do echo "$(date -u +%T) $(free -m | awk '/Mem:/{print $3, $7}')" >> "$R/mem.log"; sleep 30; done ) &
SAMP=$!
PATH="$W/.venv/bin:$PATH" VIRTUAL_ENV="$W/.venv" CARGO_PROFILE_RELEASE_LTO=false \
  CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=10 \
  nice -n 15 /usr/bin/time -v bash hp/build.sh > "$R/build.log" 2>&1
RC=$?
echo "build exit $RC $(date -u '+%F %T')" >> "$R/exits_935.txt"
kill "$SAMP"
exit "$RC"
