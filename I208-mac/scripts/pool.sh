#!/usr/bin/env bash
# pool.sh [jobs.txt]: the #208 runs, scripts/b1_row.sh on each line of the job list, at most 2 at a time, in the
# list's order (the mutation first, then the clean rows longest first). Run under nice -n 10.
set -u
D=$(cd "$(dirname "$0")" && pwd)
JOBS=${1:-$D/jobs.txt}
xargs -P 2 -n 1 "$D/b1_row.sh" < "$JOBS"
echo "pool done, xargs rc $?, $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
