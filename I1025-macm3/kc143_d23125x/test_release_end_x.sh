#!/bin/bash
# sandbox test of release_end_kc143x.sh (a fake hc, a fake chain folder, a fake driver and launcher, no real hold or driver touched): usage: bash test_release_end_x.sh [script]
# T1 a done line -> the hold files renamed (2), the fake driver started once, t5 told. T2 a STOP line, lane gone -> hold stays, no driver. T3 empty exits file, lane gone -> stays, no driver.
# T4 the scan-read line only, lane gone -> stays, no driver. T5 a done line while the driver already runs -> released, not started twice, t5 told it was running.
S=${1:-$(dirname "$0")/release_end_kc143x.sh}; SB=$(mktemp -d /private/tmp/claude-501/relendx.XXXXXX); fails=0
mkfake() { pkill -f "$SB/h/scan_chain[.]sh" 2>/dev/null; rm -rf $SB/h $SB/lg; mkdir -p $SB/h; : > $SB/h/HOLD_kc143.txt; : > $SB/h/HOLD_kc143x.txt; : > $SB/h/HOLD_low.txt.released.1
  printf '#!/bin/bash\necho "$3" >> %s/hc.out\n' $SB > $SB/hc; chmod +x $SB/hc; : > $SB/hc.out; : > $SB/lg
  printf '#!/bin/bash\nsleep 40\n' > $SB/h/scan_chain.sh
  printf '#!/bin/bash\n# fake launch_1070.py: OUT -- CMD...\nshift 2; nohup "$@" > /dev/null 2>&1 &\necho $!\n' > $SB/launch; chmod +x $SB/launch; }
run() { env NAME=kc143_d23125x LG=$SB/lg HDIR=$SB/h HC=$SB/hc LANEPAT='no-such-lane-xyz' CHAINPAT='no-such-chain-xyz' DRIVER=$SB/h/scan_chain.sh DRIVERPAT="$SB/h/scan_chain[.]sh" LAUNCH=$SB/launch REPWAIT=3 POLL=1 AFTER=1 WAITH=1 bash $S > $SB/out.txt 2>&1; }
left() { ls $SB/h | grep -c '^HOLD_kc143.*txt$'; }
drv() { pgrep -f "$SB/h/scan_chain[.]sh" | wc -l | tr -d ' '; }
mkfake; echo "== 2026 UTC kc143_d23125x ext: hc: macm3 #1025 kc143_d23125x done: [extension scan] scan: 6 evaluations" > $SB/lg; run
r=$(ls $SB/h | grep -c '^HOLD_kc143.*\.released\.'); d=$(drv)
[ "$r" = 2 ] && [ "$(left)" = 0 ] && [ "$d" -ge 1 ] && grep -q 'started again' $SB/hc.out && echo "T1 done line: released 2 files, none left, driver started ($d process lines), t5 told: ok" || { echo "T1 FAIL: released $r, left $(left), driver $d"; fails=$((fails+1)); }
for t in "T2 STOP line|== 2026 UTC kc143_d23125x: hc: macm3 #1025 kc143_d23125x STOP: the regrid not accepted" "T3 empty exits file|" "T4 scan-read line only|== 2026 UTC kc143_d23125x: hc: macm3 #1025 kc143_d23125x: the k_c 143 D 23.125 scan is read: robust changes: 2"; do
  nm=${t%%|*}; ln=${t#*|}; mkfake; [ -n "$ln" ] && echo "$ln" > $SB/lg; run
  [ "$(left)" = 2 ] && [ "$(drv)" = 0 ] && grep -q 'stays HELD' $SB/hc.out && echo "$nm: hold stays, no driver, t5 told: ok" || { echo "$nm FAIL: left $(left), driver $(drv)"; fails=$((fails+1)); }
done
mkfake; echo "== 2026 UTC kc143_d23125x: hc: macm3 #1025 kc143_d23125x done: x" > $SB/lg; ( bash $SB/h/scan_chain.sh & ) ; sleep 1; run
grep -q 'already running' $SB/hc.out && [ "$(left)" = 0 ] && echo "T5 driver already running: released, not started twice, t5 told: ok" || { echo "T5 FAIL: $(cat $SB/hc.out | cut -c1-200)"; fails=$((fails+1)); }
pkill -f "$SB/h/scan_chain[.]sh" 2>/dev/null
echo "failures: $fails"; rm -rf $SB 2>/dev/null; exit $fails
