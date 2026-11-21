#!/bin/bash
# #1064, coordinator's order of 21 Nov (~09:58 UTC): pair 1 = ks 294 from D 261.6229 and D 261.0721 side by side, then pair 2 = ks 315 from leg 10's D 260.0073 and D 259.4568 side by side;
# each instance is run1064c.sh with its own ks 293 control first (unit i1064f, g, h, i). Pair 2 starts when both units of pair 1 have ended. Caps: 8400 s per pair (2 h caps + control + deltas).
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
RAWP=I966-dh370/ks_chain3b
launch() {  # unit tag state blob K
  systemd-run --user --unit=$1 --collect --setenv=ST1064C=$3 --setenv=STBLOB1064C=$4 --setenv=TAG1064C=$2 --setenv=R_1064C=$5 /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$1 bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_$1.log $PWD/run1064c.sh 2>&1 | tail -1
}
pair() {  # unit1 tag1 state1 blob1 unit2 tag2 state2 blob2 K
  date -u '+%F %T pair start'
  launch $1 $2 $3 $4 $9; launch $5 $6 $7 $8 $9
  local t0=$(date +%s)
  while [ "$(systemctl --user is-active $1)" = active ] || [ "$(systemctl --user is-active $5)" = active ]; do
    [ $(( $(date +%s) - t0 )) -ge 8400 ] && { echo "$(date -u '+%F %T') cap on the waiter: $1 $(systemctl --user is-active $1), $5 $(systemctl --user is-active $5)"; break; }
    sleep 30
  done
  date -u '+%F %T pair end'
  for t in $2 $6; do echo "== $t"; cut -c1-200 $t/summary_1064c.txt 2>/dev/null; done
}
pair i1064f k294_D261.6229 $RAWP/leg14_D261.1415_ks293/anm_pin3_D261.6229.npz e0737904cb191e88a688df2e3968222c0920d3e5 \
     i1064g k294_D261.0721 $RAWP/leg13_D260.8483_ks293/anm_pin3_D261.0721.npz bd2c69a4d3fd16dffbc7ce340f50946772ca0b80 294
for u in i1064f i1064g; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u still active: pair 2 not started"; exit 1; }; done
pair i1064h k315_D260.0073 $RAWP/leg10_D256.1776_ks293/anm_pin3_D260.0073.npz 7d45e68357a3a622ac433857e1cf2ddc79e2410c \
     i1064i k315_D259.4568 $RAWP/leg10_D256.1776_ks293/anm_pin3_D259.4568.npz 7e2452f7d7f46275c84cd9d341d39e82d60ee0b0 315
exit 0
