#!/bin/bash
# win2: restart the k_c 103 precision check (run_prec_cheap.sh as prepared) after the hp build and its form-S selftests, the coordinator's order of 2026-11-26 ~04:40 UTC:
# "After your build and selftests, win2's next work is #1025's paused precision check (run_prec_cheap.sh as prepared: k_c 103 at 0.880 and 0.885, --noise=1e-12,1e-10 --alldd=0, cap 14 h)."
# Waits for build.done, then for the selftest chain (checks.done, or its STOP line, at most 90 min), then starts the driver through cim_start.ps1 (BelowNormal). Fires once.
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
B=/d/choptuik-i935-raw/I1025-win2/hp_form_s_build
P=/d/choptuik-i935-raw/I1025-win2/prec_k103_cheap
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a "$P/restart_events.txt"; }
[ -e "$P/restart.fired" ] && { echo "refuse: restart.fired exists"; exit 2; }
say "waiter armed: waiting for the hp build to end"
until [ -e "$B/build.done" ]; do sleep 30; done
rc=$(grep -E '^end .* exit [0-9]+' "$B/build.times" | tail -1 | sed 's/.* exit //')
say "the hp build ended with exit ${rc:-?}"
n=0
until [ -e "$B/checks.done" ] || { [ -e "$B/checks_exits.txt" ] && grep -q "STOP" "$B/checks_exits.txt"; } || [ $n -ge 180 ]; do sleep 30; n=$((n + 1)); done
say "the selftest chain: checks.done $([ -e "$B/checks.done" ] && echo present || echo absent) (waited $((n / 2)) min)"
touch "$P/restart.fired"
cd /d/choptuik-i935-raw/I1025-win2/kc71_leap
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\choptuik-i935-raw\I1025-win2\kc71_leap\cim_start.ps1" -Name prec_k103_cheap2 -Bash 'bash /d/choptuik-i935-raw/I1025-win2/prec_k103_cheap/run_prec_cheap.sh' -Dir /d/choptuik-i935-raw/I1025-win2/prec_k103_cheap 2>&1 | tee -a "$P/restart_events.txt"
say "run_prec_cheap.sh started through cim_start.ps1 (prec_k103_cheap2, BelowNormal)"
