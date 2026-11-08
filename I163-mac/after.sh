#!/bin/bash
# Issue #163: wait until a worker's stdout says its queue is done, then run a command (keeps two processes at most).
#   after.sh WORKER_STDOUT command [args...]
until grep -q "queue .* done" "$1" 2>/dev/null; do sleep 15; done
shift
exec "$@"
