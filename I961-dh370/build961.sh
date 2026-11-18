#!/bin/bash
# #961 on dh370: one hp build of perf/series-par-at 40f4b4a5 in ~/Source/choptuik-large-d-961 (fresh venv), hp/build.sh with the
# low-memory recipe (LTO off, 16 codegen units), CARGO_BUILD_JOBS=6 at nice 10 under /usr/bin/time -v. Samples system memory and
# swap (MB) every 30 s into mem961_build.log. The watcher only logs and alerts (a line in exits_961.txt and an hc message at most
# every 10 min) when swap use passes 6500 MB or MemAvailable falls below 500 MB. It never stops or kills anything.
R=/home/nathan/Source/choptuik-large-d-raw-wt613/I961-dh370
W=/home/nathan/Source/choptuik-large-d-961
cd "$W" || exit 1
echo "build start $(date -u '+%F %T') $(git log -1 --format=%h)" >> "$R/exits_961.txt"
(
  last=0
  while true; do
    read -r used avail <<< "$(free -m | awk '/Mem:/{print $3, $7}')"
    swap=$(free -m | awk '/Swap:/{print $3}')
    echo "$(date -u +%T) used $used avail $avail swap $swap" >> "$R/mem961_build.log"
    if [ "$swap" -gt 6500 ] || [ "$avail" -lt 500 ]; then
      echo "alert: avail $avail MB, swap $swap MB $(date -u '+%F %T'), nothing stopped" >> "$R/exits_961.txt"
      now=$(date +%s)
      if [ $((now - last)) -ge 600 ]; then
        last=$now
        hc send nathans-macbook-air-m5-3/t5 "dh370 #961 memory alert during the hp build: available $avail MB, swap used $swap MB, nothing stopped" > /dev/null 2>&1
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
echo "build exit $RC $(date -u '+%F %T')" >> "$R/exits_961.txt"
kill "$SAMP"
{ echo "worktree: $(git rev-parse HEAD)"; echo "python: $("$W/.venv/bin/python" -V)"; echo "date: $(date -u '+%F %T UTC')"
  "$W/.venv/bin/python" -c 'import hpkernel, multidouble; print("hpkernel.__file__", hpkernel.__file__); print("_hpkernel", hpkernel._hpkernel.__file__); print("isa", hpkernel.isa(), multidouble.isa())'
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock; } >> "$R/build961.txt" 2>&1
exit "$RC"
