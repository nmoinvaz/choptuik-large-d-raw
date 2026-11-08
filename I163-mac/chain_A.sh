#!/bin/bash
# Issue #163: what follows worker A in its slot: the checks of rt_horizon.py, then the D 60 pair test from start a.
HERE="$(cd "$(dirname "$0")" && pwd)"
"$HERE/run_checks.sh"
mkdir -p "$HERE/pair"
"$HERE/run_queue.sh" "$HERE/queue_C.txt" > "$HERE/pair/worker_C.stdout" 2>&1
