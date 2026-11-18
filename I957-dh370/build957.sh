#!/bin/bash
# #957 on dh370: one hp build of PR #956's branch (954eadcb, multishoot patched to 4e36b912), hp/build.sh with the low-memory
# recipe (LTO off, 16 codegen units, the coordinator's order), CARGO_BUILD_JOBS=6 at nice 10. Samples system memory and swap (MB) every 30 s into mem.log. The watcher
# only logs and alerts (a line in exits_957.txt and an hc message at most every 10 min) when swap use passes 6500 MB or
# MemAvailable falls below 500 MB. It never stops or kills anything.
R=/home/nathan/Source/choptuik-large-d-raw-wt613/I957-dh370
W=/home/nathan/Source/choptuik-large-d-957
cd "$W" || exit 1
echo "start $(date -u '+%F %T') $(git log -1 --format=%h)" >> "$R/exits_957.txt"
(
  last=0
  while true; do
    read -r used avail <<< "$(free -m | awk '/Mem:/{print $3, $7}')"
    swap=$(free -m | awk '/Swap:/{print $3}')
    echo "$(date -u +%T) used $used avail $avail swap $swap" >> "$R/mem.log"
    if [ "$swap" -gt 6500 ] || [ "$avail" -lt 500 ]; then
      echo "alert: avail $avail MB, swap $swap MB $(date -u '+%F %T'), nothing stopped" >> "$R/exits_957.txt"
      now=$(date +%s)
      if [ $((now - last)) -ge 600 ]; then
        last=$now
        hc send nathans-macbook-air-m5-3/t5 "dh370 #957 memory alert during the hp build: available $avail MB, swap used $swap MB, nothing stopped" > /dev/null 2>&1
      fi
    fi
    sleep 30
  done
) &
SAMP=$!
PATH="$W/.venv/bin:$PATH" VIRTUAL_ENV="$W/.venv" CARGO_BUILD_JOBS=6 CARGO_PROFILE_RELEASE_LTO=false \
  CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 \
  nice -n 10 /usr/bin/time -v bash hp/build.sh > "$R/build.log" 2>&1
RC=$?
echo "build exit $RC $(date -u '+%F %T')" >> "$R/exits_957.txt"
kill "$SAMP"
exit "$RC"
