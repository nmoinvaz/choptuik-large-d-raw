#!/usr/bin/env python3
"""mk_rs.py [--write] : t5's order (hc 04:23 UTC 27 Nov, #1102): the D 23.125 lane's scan and secant with --b12=rust --b12_threads=4 (ellrs, worktree 1102m3 at d4b6b6ce, SITE ~/Source/ellrs-site-1102m3).
Builds, by ordered asserted replacements (each must occur the stated number of times), kc87_leg_lambda/pointnew_rs.sh from pointnew.sh and lane_d23125.sh from its Python-block-12 original
(kept as lane_d23125_python.sh). Without --write the results go to rust_b12/draft/ only; --write puts them in place (the original lane is copied first; refuses when lane_d23125_python.sh exists).
The diffs are read before the lane starts (rust_b12/diff_lane_rs.txt, diff_pointnew_rs.txt)."""
import os, shutil, subprocess, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
F = R + "kc143_d23125/"; L = R + "kc87_leg_lambda/"; H = F + "rust_b12/"
SOLHASH = "d2221460d02c"      # sha256 of ellrs.cpython-314-darwin.so in the SITE folder (first 12), from the build of 04:26 UTC


def rep(t, old, new, n=1):
    c = t.count(old)
    assert c == n, "%r occurs %d times, expected %d" % (old[:80], c, n)
    return t.replace(old, new)


def pointnew(t):
    t = rep(t, "WT=$HOME/Source/choptuik-large-d-1025s2; WTM=$WT/solver/matter;", "WT=$HOME/Source/choptuik-large-d-1102m3; WTM=$WT/solver/matter; SITE=$HOME/Source/ellrs-site-1102m3; B12T=${B12T:-4};")
    t = rep(t, "VECLIB_MAXIMUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1\ncd $OUT", "VECLIB_MAXIMUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONPATH=$SITE PYTHONFAULTHANDLER=1\ncd $OUT")
    t = rep(t, '[ "$(blob $WTM/d18_secant.py)" = eb1396ad ] || stop "d18_secant.py of the worktree is not blob eb1396ad"',
            '[ "$(blob $WTM/d18_secant.py)" = 9706e506 ] || stop "d18_secant.py of the worktree is not blob 9706e506"\n'
            '[ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "ell_b12rs.py of the worktree is not blob a1fff74f"\n'
            '[ "$(shasum -a 256 $SITE/ellrs/ellrs.cpython-314-darwin.so | cut -c1-12)" = @SOL@ ] || stop "the ellrs module in $SITE is not the one gated (sha256 @SOL@)"'.replace("@SOL@", SOLHASH))
    t = rep(t, "the scanner d18_secant.py eb1396ad (worktree 92b9bf53)", "the scanner d18_secant.py 9706e506 with ell_b12rs.py a1fff74f and ellrs (sha256 %s) from $SITE (worktree d4b6b6ce, branch wip/ell1-rust-b12)" % SOLHASH)
    t = rep(t, '[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 92b9bf53 ] || stop "worktree not at 92b9bf53"', '[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = d4b6b6ce ] || stop "worktree not at d4b6b6ce"')
    t = rep(t, 'step "worktree 92b9bf53 (dss_ell', 'step "worktree d4b6b6ce (dss_ell')
    t = rep(t, "on $NP processes of 1 thread, nice", "on $NP processes of 1 float64 thread and $B12T block-12 threads (--b12=rust), nice")
    t = rep(t, "OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1 \\\n      $PY -u $L/common/capped_run.py 28800 $PY -u $WTM/d18_secant.py scan $STUB $STATE $D \"$mine\" $OUT/scan/scan_D${D}_p$p.jsonl --pin=$STATEBLOB,$RECBLOB >",
            "OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONFAULTHANDLER=1 \\\n      $PY -u $L/common/capped_run.py 28800 $PY -u $WTM/d18_secant.py scan $STUB $STATE $D \"$mine\" $OUT/scan/scan_D${D}_p$p.jsonl --pin=$STATEBLOB,$RECBLOB --b12=rust --b12_threads=$B12T >")
    head = ("#!/bin/bash\n# pointnew_rs.sh: pointnew.sh with block 12 in Rust (t5, hc 04:23 UTC 27 Nov, #1102): worktree 1102m3 at d4b6b6ce (d18_secant.py 9706e506, ell_b12rs.py a1fff74f), ellrs from ~/Source/ellrs-site-1102m3, "
            "the scan command with --b12=rust --b12_threads=$B12T (default 4) and without RAYON_NUM_THREADS=1. Made by kc143_d23125/mk_rs.py from pointnew.sh (asserted replacements); the comments below are pointnew.sh's.\n")
    assert t.startswith("#!/bin/bash\n")
    return head + t[len("#!/bin/bash\n"):]


def lane(t):
    t = rep(t, "WTS=$HOME/Source/choptuik-large-d-1025s2/solver/matter\n", "WTS=$HOME/Source/choptuik-large-d-1102m3/solver/matter; SITE=$HOME/Source/ellrs-site-1102m3   # Rust block 12 (t5, hc 04:23 UTC 27 Nov, #1102): the scanner worktree is the branch's\n")
    t = rep(t, '[ "$(git -C ${WTS%/solver/matter} rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTS/d18_secant.py | cut -c1-8)" = eb1396ad ] || stop "the scanner worktree is not at 92b9bf53 with d18_secant.py eb1396ad"',
            '[ "$(git -C ${WTS%/solver/matter} rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ "$(blob $WTS/d18_secant.py | cut -c1-8)" = 9706e506 ] || stop "the scanner worktree is not at d4b6b6ce with d18_secant.py 9706e506"\n'
            '[ "$(blob $WTS/ell_b12rs.py | cut -c1-8)" = a1fff74f ] && [ -z "$(git -C ${WTS%/solver/matter} status --short solver)" ] || stop "ell_b12rs.py is not a1fff74f or the scanner worktree is not clean"\n'
            '[ "$(shasum -a 256 $SITE/ellrs/ellrs.cpython-314-darwin.so | cut -c1-12)" = @SOL@ ] || stop "the ellrs module in $SITE is not the one gated (sha256 @SOL@)"'.replace("@SOL@", SOLHASH))
    t = rep(t, "and the scanner worktree 92b9bf53 (d18_secant.py eb1396ad)", "and the scanner worktree d4b6b6ce (d18_secant.py 9706e506, ell_b12rs.py a1fff74f, ellrs sha256 %s in $SITE)" % SOLHASH)
    t = rep(t, "( cd $WTS && export RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1\n", "( cd $WTS && export PYTHONPATH=$SITE RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1\n")
    t = rep(t, '  echo "$nx" > $C/newscan_exits.txt )',
            '  for m in "" nolam harm; do nice -n 10 $PY ell_b12rs.py selftest ${m:+--mutate=$m} > $C/b12rs_selftest${m:+_$m}.txt 2>&1; nx="$nx $?"; done\n  echo "$nx" > $C/newscan_exits.txt )')
    t = rep(t, '[ "$(cat $C/newscan_exits.txt)" = "0 1 1 1" ] || stop "the new scanner\'s selftest exits \'$(cat $C/newscan_exits.txt)\' (wanted \'0 1 1 1\': selftest, half, norobust, nosigncheck)"',
            '[ "$(cat $C/newscan_exits.txt)" = "0 1 1 1 0 1 1" ] || stop "the new scanner\'s and ell_b12rs\'s selftest exits \'$(cat $C/newscan_exits.txt)\' (wanted \'0 1 1 1 0 1 1\': selftest, half, norobust, nosigncheck, ell_b12rs selftest, nolam, harm)"')
    t = rep(t, "worktree 92b9bf53): selftest exit 0, --mutate=half exit 1, --mutate=norobust exit 1, --mutate=nosigncheck exit 1 (logged before the scan, as t5 ordered)",
            "worktree d4b6b6ce): selftest exit 0, --mutate=half exit 1, --mutate=norobust exit 1, --mutate=nosigncheck exit 1; ell_b12rs.py selftest exit 0, --mutate=nolam exit 1, --mutate=harm exit 1 (logged before the scan, as t5 ordered)")
    t = rep(t, "bash $L/pointnew.sh $DN scan >>", "bash $L/pointnew_rs.sh $DN scan >>")
    t = rep(t, 'say "scan starts (pointnew.sh $DN scan: the new scanner d18_secant.py scan)"', 'say "scan starts (pointnew_rs.sh $DN scan: the scanner d18_secant.py scan with --b12=rust --b12_threads=4)"')
    t = rep(t, "( cd $WTS && env RAYON_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10", "( cd $WTS && env PYTHONPATH=$SITE OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10")
    t = rep(t, "$SEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB > $SEC/secant.log", "$SEC/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4 > $SEC/secant.log")
    t = rep(t, 'say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB"', 'say "secant starts: d18_secant.py run $S_REC $S_STATE $D $LO $HI secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$TB --b12=rust --b12_threads=4"')
    t = rep(t, "#!/bin/bash\n", "#!/bin/bash\n# RUST BLOCK 12 (t5, hc 04:23 UTC 27 Nov 2026, #1102): the scan (pointnew_rs.sh) and the secant of this lane run with --b12=rust --b12_threads=4 (ellrs in ~/Source/ellrs-site-1102m3, worktree 1102m3 at d4b6b6ce, d18_secant.py 9706e506); changes read in rust_b12/diff_lane_rs.txt and the README.\n")
    return t


def main():
    write = "--write" in sys.argv
    os.makedirs(H + "draft", exist_ok=True)
    pn = pointnew(open(L + "pointnew.sh").read())
    orig = F + "lane_d23125_python.sh" if os.path.exists(F + "lane_d23125_python.sh") else F + "lane_d23125.sh"
    assert not (write and os.path.exists(F + "lane_d23125_python.sh")), "lane_d23125_python.sh exists: already applied"
    ln = lane(open(F + "lane_d23125.sh").read())
    open(H + "draft/pointnew_rs.sh", "w").write(pn); open(H + "draft/lane_d23125.sh", "w").write(ln)
    d1 = subprocess.run(["diff", L + "pointnew.sh", H + "draft/pointnew_rs.sh"], capture_output=True, text=True).stdout
    d2 = subprocess.run(["diff", F + "lane_d23125.sh", H + "draft/lane_d23125.sh"], capture_output=True, text=True).stdout
    open(H + "diff_pointnew_rs.txt", "w").write(d1); open(H + "diff_lane_rs.txt", "w").write(d2)
    print("draft written; diff lines: pointnew %d, lane %d" % (d1.count("\n"), d2.count("\n")))
    if write:
        shutil.copy2(F + "lane_d23125.sh", F + "lane_d23125_python.sh")
        shutil.copy2(H + "draft/lane_d23125.sh", F + "lane_d23125.sh"); os.chmod(F + "lane_d23125.sh", 0o755)
        shutil.copy2(H + "draft/pointnew_rs.sh", L + "pointnew_rs.sh"); os.chmod(L + "pointnew_rs.sh", 0o755)
        print("written: lane_d23125.sh (original kept as lane_d23125_python.sh), kc87_leg_lambda/pointnew_rs.sh")


if __name__ == "__main__":
    main()
