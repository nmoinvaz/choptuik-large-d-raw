#!/bin/bash
# exits when r0.exit exists, or when all three exit files exist; prints state
HERE=$(cd "$(dirname "$0")" && pwd)
until [ -f "$HERE/r0.exit" ]; do sleep 20; done
date -u '+%Y-%m-%d %H:%M:%S UTC r0 ended'
cat "$HERE/r0.exit"
tail -4 "$HERE/r0.out" | cut -c1-300
