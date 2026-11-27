#!/usr/bin/env python3
"""mk_kmm.py : makes pointkmm.sh of I1101-macm3/ from kc87_leg_lambda/pointnew_rs.sh (the Rust-block scan driver of the chain and of every lane since 27 Nov), with every replacement asserted: the scanner worktree
choptuik-large-d-kmm at f56f91d2 (wip/ell1-kappa-mm, d18_secant.py 2f3ee874: --kappa_mm), the option --kappa_mm=$KMM on the scan command (KMM from point.env), no repeat required when REP is empty (the kappa_mm 0.5 control stands in for it).
The unified diff goes to diff_pointkmm.txt."""
import os, subprocess
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/")
B = R + "I1025-macm3/kc87_leg_lambda/pointnew_rs.sh"; X = R + "I1101-macm3/"
s = open(B).read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old, s.count(old), n)
    s = s.replace(old, new)
rep("# pointnew_rs.sh: pointnew.sh with block 12 in Rust", "# pointkmm.sh (I1101, t5's order of 27 Nov 16:3x UTC, #1101 comment 7223316450): pointnew_rs.sh with the scanner of wip/ell1-kappa-mm (worktree choptuik-large-d-kmm at f56f91d2, d18_secant.py 2f3ee874, --kappa_mm=$KMM from point.env), no repeat required when REP is empty. Below, the header of pointnew_rs.sh:\n# pointnew_rs.sh: pointnew.sh with block 12 in Rust")
rep("WT=$HOME/Source/choptuik-large-d-1102m3;", "WT=$HOME/Source/choptuik-large-d-kmm;")
rep('[ "$(blob $WTM/d18_secant.py)" = 9706e506 ] || stop "d18_secant.py of the worktree is not blob 9706e506"', '[ "$(blob $WTM/d18_secant.py)" = 2f3ee874 ] || stop "d18_secant.py of the worktree is not blob 2f3ee874"')
rep('[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = d4b6b6ce ] || stop "worktree not at d4b6b6ce"', '[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = f56f91d2 ] || stop "worktree not at f56f91d2"')
rep("the scanner d18_secant.py 9706e506 with ell_b12rs.py a1fff74f and ellrs (sha256 d2221460d02c) from $SITE (worktree d4b6b6ce, branch wip/ell1-rust-b12)", "the scanner d18_secant.py 2f3ee874 with ell_b12rs.py a1fff74f and ellrs (sha256 d2221460d02c) from $SITE (worktree f56f91d2, branch wip/ell1-kappa-mm)")
rep('step "worktree d4b6b6ce (dss_ell', 'step "worktree f56f91d2 (dss_ell')
rep('R1=-1; R2=-1; for ((i = 0; i < ${#LAMP[@]}; i++)); do [ "${LAMP[$i]}" = "$REP" ] && { [ $R1 -lt 0 ] && R1=$i || R2=$i; }; done\n[ $R2 -ge 0 ] && [ $((R1 % NP)) != $((R2 % NP)) ] || stop "the repeat of $REP is not on another process than the first"',
    'R1=-1; R2=-1; if [ -n "$REP" ]; then for ((i = 0; i < ${#LAMP[@]}; i++)); do [ "${LAMP[$i]}" = "$REP" ] && { [ $R1 -lt 0 ] && R1=$i || R2=$i; }; done\n[ $R2 -ge 0 ] && [ $((R1 % NP)) != $((R2 % NP)) ] || stop "the repeat of $REP is not on another process than the first"; fi')
rep("--pin=$STATEBLOB,$RECBLOB --b12=rust --b12_threads=$B12T > $OUT/scan/scan_p$p.log", "--pin=$STATEBLOB,$RECBLOB --b12=rust --b12_threads=$B12T --kappa_mm=$KMM > $OUT/scan/scan_p$p.log")
rep("the first $REP on process $((R1 % NP)), the repeat on process $((R2 % NP));", "kappa_mm $KMM; the repeat (REP '${REP:-none}') on process $((R1 % NP)) and $((R2 % NP)) (-1: none);")
rep("macm3 #1025 kc87_leg_lambda ALERT", "macm3 #1101 kmm ALERT")
open(X + "pointkmm.sh", "w").write(s)
d = subprocess.run(["diff", "-u", B, X + "pointkmm.sh"], capture_output=True, text=True).stdout
open(X + "diff_pointkmm.txt", "w").write(d); print("pointkmm.sh written; diff lines", len(d.splitlines()))
