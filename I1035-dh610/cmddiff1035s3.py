#!/usr/bin/env python3
"""cmddiff1035s3.py --actual CMD [--var B293=PATH --var B=PATH] [--ref FILE] | --selftest [--break]: the diff of a command line against §5.3's commands block (ref/section53_commands_ebc96296.txt, the block of notes/FACTORED_HORIZON.md at
ebc96296, verbatim), before each launch of stage 3 (the coordinator's rule of 21 Nov, after three slips). Both are reduced to the tokens of the factored_raise.py / anm_run.py / exact_recip_check.py invocation (`timeout`, `nice`, the redirection and the comment
dropped; $RAW, $OUT (= .../I1035-dh610/stage2), $P0, $PR, $S3, $L14, $B293, $B and <machine> (dh610) expanded from the block's own assignments), the reference line is found by its key (script, subcommand, output folder), and the token lists are diffed
(unified, one token a line). $B293 may also be $S3 (the polish was skipped) and $B the raised state (the block says so): --var gives the value the harness used and the tool accepts it only as one of those two. Prints the diff and 'cmddiff KEY: EMPTY' or
'DIFFERS' or 'NOREF'; exit 0 only when empty. L14 is the block's own (the harness reads it from the same file), so the diff checks everything but the L14 text. --selftest plants slips (a dropped --mutate, a changed --tol, --ks, --steps, state, an L14 flag, a
polishgate folder) which must each differ, and the correct commands, which must be empty; --break expects a slip to be empty and must exit 1."""
import difflib
import os
import re
import shlex
import sys

RAW = "/home/nathan/Source/choptuik-large-d-raw"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = f"{RAW}/I1035-dh610/stage2"
REFFILE = os.path.join(HERE, "ref", "section53_commands_ebc96296.txt")
SCRIPTS = ("factored_raise.py", "anm_run.py", "exact_recip_check.py")


def assigns(ref):
    v = {}
    for line in open(ref):
        m = re.match(r'^([A-Z0-9]+)=("([^"]*)"|(\S+))', line)
        if m:
            v[m.group(1)] = (m.group(3) if m.group(3) is not None else m.group(4)).replace("<machine>", "dh610")
    return v


def expand(cmd, v, override=None):
    cmd = cmd.replace("<machine>", "dh610").replace("$OUT", OUT).replace("$RAW", RAW)
    vv = dict(v)
    vv.update(override or {})
    for k in sorted(vv, key=len, reverse=True):
        cmd = re.sub(r"\$" + k + r"(?![A-Za-z0-9_])", lambda m, k=k: vv[k], cmd)
    return cmd


def tokens(cmd):
    m = re.search(r"(factored_raise\.py|anm_run\.py|exact_recip_check\.py)(.*)$", cmd)
    if not m:
        return None
    rest = re.split(r"\s>\s|\s2>&1|;|\s#", m.group(2))[0]
    return [m.group(1)] + shlex.split(rest)


def key(t):
    sub = t[1] if len(t) > 1 and t[1] in ("selftest", "polishgate", "stepgate", "delta") else ""
    if sub in ("polishgate", "stepgate"):
        folder = t[-1]
    elif sub == "delta":
        folder = t[t.index("--out") + 1] if "--out" in t else ""
    elif sub == "selftest":
        folder = " ".join(x for x in t[3:] if x.startswith("--"))
    else:
        folder = next((x for x in t[1:] if x.startswith(OUT + "/") and not x.endswith(".log")), "")
    return (t[0], sub, folder)


def reference(ref, override=None):
    v = assigns(ref)
    d = {}
    for line in open(ref):
        if line.startswith("#"):
            continue
        t = tokens(expand(line.rstrip("\n"), v, override))
        if t:
            d[key(t)] = t
    return d, v


def diff(actual, ref=REFFILE, var=None):
    v = assigns(ref)
    var = var or {}
    allowed = {"B293": {v.get("B293"), v.get("S3")}, "B": {v.get("B"), f"{OUT.split('/I1035')[0].split('/')[-1] and 'I1035-dh610/stage2/real/raise_pin3_D262.0099.npz'}"}}
    for k, val in var.items():
        if val not in allowed.get(k, set()):
            return None, f"--var {k}={val} is not one of the block's alternatives {sorted(x for x in allowed.get(k, set()) if x)}"
    refd, _ = reference(ref, var)
    a = tokens(actual)
    if a is None:
        return None, "no factored_raise.py / anm_run.py / exact_recip_check.py invocation in the actual command"
    k = key(a)
    if k not in refd:
        return None, f"NOREF {k}"
    return list(difflib.unified_diff(refd[k], a, "section 5.3", "actual", lineterm="", n=1)), None


def selftest(brk):
    v = assigns(REFFILE)
    L14 = v["L14"]
    S3, B293, B = v["S3"], v["B293"], v["B"]
    good = {
        "real": f"timeout -s TERM 14400 nice -n 10 python3 -u factored_raise.py {RAW} {OUT}/real --state {S3} --ks 315 --threads 10 --tol 1e-50",
        "real_old": f"nice -n 10 python3 -u factored_raise.py {RAW} {OUT}/real_old --state {S3} --ks 315 --threads 10 --tol 1e-50 --mutate=old",
        "polish293": f"nice -n 10 python3 -u anm_run.py {RAW} {OUT}/polish293 --state {S3} {L14} --steps 0 --ks 293 --keep_plan 1 --save_base 1",
        "step293": f"nice -n 10 python3 -u anm_run.py {RAW} {OUT}/step293 --state {B293} {L14} --steps 1 --ks 293 --keep_plan 1",
        "gate": f"python3 factored_raise.py polishgate {OUT}/polish293.log {OUT}/polish293",
        "polish315": f"nice -n 10 python3 -u anm_run.py {RAW} {OUT}/polish315 --state I1035-dh610/stage2/real/raise_pin3_D262.0099.npz {L14} --steps 0 --ks 315 --keep_plan 1 --save_base 1",
        "delta": f"python3 exact_recip_check.py delta {RAW}/{S3} {RAW}/{B} --out {OUT}/delta_315_vs_293.json",
    }
    slips = [("real_old without --mutate=old (the slip of 21 Nov)", good["real_old"].replace(" --mutate=old", "")), ("real with --tol 1e-60", good["real"].replace("1e-50", "1e-60")),
             ("polish293 with --ks 315", good["polish293"].replace("--ks 293", "--ks 315")), ("step293 with --steps 0", good["step293"].replace("--steps 1", "--steps 0")),
             ("step293 on the wrong state", good["step293"].replace(B293, v["S3"].replace("262.0099", "262.7908"))), ("polish293 with --tol_od 1e-60", good["polish293"].replace("--tol_od 2e-34", "--tol_od 1e-60")),
             ("polishgate on the wrong folder", good["gate"].replace("polish293 ", "polish315 ").replace(OUT + "/polish293.log", OUT + "/polish293.log").replace("polish293.log", "polish293.log")[:-9] + "polish315"),
             ("real_old on the ks 293 state", good["real_old"].replace("--ks 315", "--ks 293"))]
    bad = 0
    for name, c in good.items():
        d, e = diff(c)
        ok = e is None and d == []
        print(f"  correct {name}: {'empty' if d == [] else (d[:3] if d else e)}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    for name, c in slips:
        d, e = diff(c)
        want_empty = brk and name.startswith("real_old without")
        ok = e is None and ((d == []) if want_empty else bool(d))
        print(f"  slip {name}: {'empty' if d == [] else ('differs' if d else e)} (expected {'empty' if want_empty else 'differs'}): {'ok' if ok else 'WRONG'}")
        bad += not ok
    d, e = diff(good["step293"], var={"B293": v["S3"]})
    ok = e is None and d == [] or (e is None and d)
    d2, e2 = diff(good["step293"], var={"B293": "some/other.npz"})
    ok2 = e2 is not None
    print(f"  --var B293 an allowed alternative accepted; a foreign path refused: {'ok' if ok and ok2 else 'WRONG'}")
    bad += not (ok and ok2)
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    var = {}
    for i, a in enumerate(sys.argv):
        if a == "--var":
            k, _, val = sys.argv[i + 1].partition("=")
            var[k] = val
    actual = sys.argv[sys.argv.index("--actual") + 1]
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else REFFILE
    d, err = diff(actual, ref, var)
    if d is None:
        print(f"cmddiff: ERROR {err}")
        sys.exit(2)
    t = tokens(actual)
    for l in d:
        print(l)
    print(f"cmddiff {key(t)}: {'EMPTY' if not d else 'DIFFERS'}")
    sys.exit(0 if not d else 1)
