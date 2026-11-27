#!/bin/bash
# sandbox test of release_end_kc143b.sh (a fake hc, a fake chain folder, no real hold touched): usage: bash test_release_end.sh [script]   (default release_end_kc143b.sh)
# T1 a done line -> the hold file(s) renamed (wanted: released, 2 files). T2 a STOP line, lane gone -> hold stays. T3 empty exits file, lane gone -> hold stays. T4 the scan-read line only, lane gone -> hold stays.
S=${1:-$(dirname "$0")/release_end_kc143b.sh}; SB=$(mktemp -d /private/tmp/claude-501/relend.XXXXXX); fails=0
mkfake() { rm -rf $SB/h $SB/lg; mkdir -p $SB/h; : > $SB/h/HOLD_kc143.txt; : > $SB/h/HOLD_kc143b.txt; : > $SB/h/HOLD_low.txt.released.1; printf '#!/bin/bash\necho "$3" >> %s/hc.out\n' $SB > $SB/hc; chmod +x $SB/hc; : > $SB/hc.out; : > $SB/lg; }
run() { env NAME=kc143_d23125 LG=$SB/lg HDIR=$SB/h HC=$SB/hc LANEPAT='no-such-lane-xyz' CHAINPAT='no-such-chain-xyz' REPWAIT=3 POLL=1 AFTER=1 WAITH=1 bash $S > $SB/out.txt 2>&1; }
left() { ls $SB/h | grep -c '^HOLD_kc143.*txt$'; }
mkfake; echo "== 2026 UTC kc143_d23125: hc: macm3 #1025 kc143_d23125 done: scan: 6 evaluations" > $SB/lg; run
r=$(ls $SB/h | grep -c '^HOLD_kc143.*\.released\.'); [ "$r" = 2 ] && [ "$(left)" = 0 ] && echo "T1 done line: released 2 files, none left: ok" || { echo "T1 FAIL: released $r, left $(left)"; fails=$((fails+1)); }
for t in "T2 STOP line|== 2026 UTC kc143_d23125: hc: macm3 #1025 kc143_d23125 STOP: the regrid not accepted" "T3 empty exits file|" "T4 scan-read line only|== 2026 UTC kc143_d23125: hc: macm3 #1025 kc143_d23125: the k_c 143 D 23.125 scan is read: robust changes 2"; do
  nm=${t%%|*}; ln=${t#*|}; mkfake; [ -n "$ln" ] && echo "$ln" > $SB/lg; run
  [ "$(left)" = 2 ] && grep -q 'stays HELD' $SB/hc.out && echo "$nm: hold stays, t5 told: ok" || { echo "$nm FAIL: left $(left)"; fails=$((fails+1)); }
done
echo "failures: $fails"; rm -rf $SB 2>/dev/null; exit $fails
