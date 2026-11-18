#!/bin/bash
# withmem967.sh LOG SCRIPT [ARGS...]: runs SCRIPT with the alert-only memory log (memlog967.sh) watching this process
D=$(cd "$(dirname "$0")" && pwd)
LOG=$1; shift
bash "$D/memlog967.sh" "$LOG" $$ 30 &
exec bash "$@"
