#!/bin/bash
# #1058: the build script's watchdog is alert-only. Positive control: thresholds above the current MemAvailable, the "build" is `sleep 6; exit 7`: the 3 alert levels fire,
# the build is not stopped and its own exit 7 comes through (a jump over all three levels is reported once, at level 3; one level above gives one alert at level 1).
# Negative control: thresholds of 1 KB: no alert. usage: bash selftest_build1058.sh (exit 0 when all hold)
H=/home/nathan/Source/choptuik-large-d-raw/I1058-dh170
T=$(mktemp -d /home/nathan/scratch1058/selftest.XXXXXX)
ok=1
run() {  # name, L1 L2 L3
  mkdir -p $T/$1; T1058_TEST=$T/$1 T1058_HCSEND="echo HC" T1058_BUILD_CMD="sleep 6; exit 7" T_L1=$2 T_L2=$3 T_L3=$4 bash $H/build1058.sh > $T/$1/out.txt 2>&1; echo $? > $T/$1/rc
}
a=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
run pos $((a+3000000)) $((a+2000000)) $((a+1000000))
run one $((a+3000000)) 1 1
run neg 1 1 1
npos=$(grep -c '^ALERT' $T/pos/alert1058.log 2>/dev/null); nneg=$(grep -c '^ALERT' $T/neg/alert1058.log 2>/dev/null); none=$(grep -c '^ALERT' $T/one/alert1058.log 2>/dev/null)
npos=${npos:-0}; nneg=${nneg:-0}; none=${none:-0}
lpos=$(grep -o 'level [0-9]' $T/pos/alert1058.log | head -1); lone=$(grep -o 'level [0-9]' $T/one/alert1058.log | head -1)
rpos=$(cat $T/pos/rc); rone=$(cat $T/one/rc); rneg=$(cat $T/neg/rc)
sleep 1
echo "positive control, all three thresholds above MemAvailable $((a/1024)) MB: $npos ALERT line at $lpos (want 1 at level 3), build exit $rpos (want 7, nothing stopped), hc lines $(grep -c HC $T/pos/hc_sent.log 2>/dev/null) (want 1)"
echo "positive control, only the 2 GiB threshold above: $none ALERT line at $lone (want 1 at level 1), build exit $rone (want 7)"
echo "negative control (thresholds 1 KB): $nneg ALERT lines (want 0), build exit $rneg (want 7)"
[ "$npos" = 1 ] && [ "$lpos" = "level 3" ] && [ "$rpos" = 7 ] && [ "$none" = 1 ] && [ "$lone" = "level 1" ] && [ "$rone" = 7 ] && [ "$nneg" = 0 ] && [ "$rneg" = 7 ] || ok=0
echo "selftest_build1058: $([ $ok = 1 ] && echo pass || echo FAIL)  (scratch $T)"
[ $ok = 1 ]
