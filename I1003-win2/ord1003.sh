#!/usr/bin/env bash
# #1003 K 49: per-order record, read only. The python's own log lines after order 25 are lost: my `git pull --rebase` in this worktree at 10:16:19 UTC on 2026-11-19 replaced the log file under the running process.
# The .partial.json (os.replace per order) is not affected. This glue appends "UTC k_done seconds n_sigma" to orders_1003.log whenever k_done changes, and ends when the python (pid in k49.winpid) is gone.
# usage: bash ord1003.sh
X=/d/choptuik-large-d-raw-743/I1003-win2
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
P=D:/choptuik-large-d-raw-743/I1003-win2/sigF_w1.0000_K49_J1500_p1280.json.partial.json
W=$(cat $X/k49.winpid)
alive() { powershell -NoProfile -Command "if (Get-Process -Id $W -ErrorAction SilentlyContinue) { 'yes' } else { 'no' }" | tr -d '\r'; }
last=""
while [ "$(alive)" = "yes" ]; do
  cur=$("$PY" -I -c "import json,sys;d=json.load(open(sys.argv[1]));print(d['k_done'],d['seconds'],len(d['sigma_str']))" "$P" 2>/dev/null)
  if [ -n "$cur" ] && [ "${cur%% *}" != "${last%% *}" ]; then
    echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') k_done seconds n_sigma: $cur" >> $X/orders_1003.log
    last="$cur"
  fi
  sleep 60
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') K 49 python gone, recorder ends" >> $X/orders_1003.log
