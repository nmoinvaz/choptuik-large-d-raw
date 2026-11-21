#!/bin/bash
# #1064, the coordinator's change (11:5x UTC 21 Nov): the re-seeded-base rungs are ks 315 at D 261.6229 (unit i1064k) and at D 262.0099 (unit i1064l), each after its own ks 293 control with --reseed_base 1 (run1064d.sh, main 276aa1cd)
cd ~/Source/choptuik-large-d-raw/I1064-dh610 || exit 1
for u in i1064j i1064k i1064l; do [ "$(systemctl --user is-active $u)" = active ] && { echo "$u active: not started"; exit 1; }; done
RAWP=I966-dh370/ks_chain3b/leg14_D261.1415_ks293
launch() {  # unit tag state blob earlier earlier0
  systemd-run --user --unit=$1 --collect --setenv=ST1064D=$3 --setenv=STBLOB1064D=$4 --setenv=TAG1064D=$2 --setenv=R_1064D=315 --setenv=EARLIER1064D=$5 --setenv=EARLIER0_1064D=$6 /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$1 bash $PWD/../I967-dh610/withmem967.sh $PWD/memlog_$1.log $PWD/run1064d.sh 2>&1 | tail -1
}
date -u '+%F %T start'
launch i1064k rb_D261.6229 $RAWP/anm_pin3_D261.6229.npz e0737904cb191e88a688df2e3968222c0920d3e5 $PWD/k294_D261.6229/ks293/base_pin3_D261.6229.npz $PWD/leg14_D261.6229/ks293/base_pin3_D261.6229.npz
launch i1064l rb_D262.0099 $RAWP/anm_pin3_D262.0099.npz eb34f3c845a485d606907b6f7ba2dc9ef429aaf1 $PWD/../$RAWP/anm_pin3_D262.0099.npz $PWD/../$RAWP/anm_pin3_D262.0099.npz
