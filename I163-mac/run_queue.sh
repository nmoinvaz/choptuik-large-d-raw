#!/bin/bash
# Issue #163: a worker that runs the lines of a queue file in order, each "OUTDIR TAG START GRID K [opts]" for
# run_one.sh. Two workers run at once (the Mac is shared).
#   run_queue.sh QUEUEFILE
HERE="$(cd "$(dirname "$0")" && pwd)"
while read -r OUT TAG ST G K REST; do
    [ -z "$OUT" ] && continue
    case "$OUT" in \#*) continue ;; esac
    "$HERE/run_one.sh" "$OUT" "$TAG" "$ST" "$G" "$K" $REST
done < "$1"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC queue $1 done"
