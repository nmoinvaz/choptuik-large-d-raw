#!/bin/bash
# #1070 (coordinator's hc ~22:27 UTC 21 Nov): gamma at D 3.15 at M 160 on dh170, hp/lowD_gamma.py, beside macm3b's M 128 with the same lam0 (4.3977): --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977, nice 10, 6 h cap
# (timeout -s TERM 21600, by pid), output here. Usage: run_1070_dh170.sh   (DRY=1 prints the command and exits)
P=/home/nathan/Source/choptuik-large-d-raw-1064w/I1070-dh170
WT=/home/nathan/Source/choptuik-large-d-1058b
PY=$WT/.venv/bin/python
IN=/home/nathan/scratch1070/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz
OUT=$P/lowD_gamma_D3.15_M160.jsonl
CMD="$PY -u hp/lowD_gamma.py $OUT $IN --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977"
[ -n "$DRY" ] && { echo "$CMD"; exit 0; }
export PYTHONFAULTHANDLER=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PATH=$WT/.venv/bin:$PATH VIRTUAL_ENV=$WT/.venv
say() { echo "== $(date -u '+%F %T') UTC $*" >> $P/exits_1070.txt; }
[ -e $OUT ] && { say "refuse: $OUT exists (no overwrite)"; exit 3; }
[ -e $P/run_M160.log ] && { say "refuse: run_M160.log exists (no overwrite)"; exit 3; }
[ "$(git hash-object --no-filters $IN)" = 2515013d1ed23e09e5ca7d4aee82ac5781f72d12 ] || { say "refuse: input blob is not 2515013d"; exit 2; }
cd $WT || exit 9
HK=$($PY -c "import hpkernel, sys; print('hpkernel', hpkernel.__file__, 'isa', hpkernel.isa(), 'python', sys.version.split()[0])" 2>&1 | tr '\n' ' ')
say "M160 start, code $(git rev-parse --short HEAD) (hp/lowD_gamma.py at 8179068d), venv $PY: $HK; input blob 2515013d1ed2, cap 21600 s, command: $CMD"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout -s TERM 21600 $CMD > $P/run_M160.log 2>&1 &
tp=$!
while kill -0 $tp 2>/dev/null; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  py=$(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null | head -1); rss=0; cpu=0
  [ -n "$py" ] && { rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null); cpu=$(ps -o pcpu= -p $py | tr -d ' '); }
  echo "$(date -u '+%T') MemAvailable $av MiB, lowD_gamma pid ${py:-none} RSS ${rss:-0} MiB cpu ${cpu:-0}%" >> $P/memlog_M160.log
  [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') MemAvailable $av MiB (alert only)" >> $P/alert_M160.log
  sleep 60
done
wait $tp; rc=$?
say "M160 exit $rc, $(( $(date +%s) - s0 )) s wall"
[ -e $OUT ] && say "M160 acceptance: $($PY -I $P/accept_1070.py $OUT)" || say "M160 acceptance: no record written"
say "done"
