#!/usr/bin/env python3
"""mk_lanes143.py : writes the two k_c 143 lanes of #1025 (t5's order, hc 27 Nov 01:38 UTC) from kc135_d23125/lane_d23125.sh by explicit ordered replacements, and their input folders.
  kc143_d230625: k_c 143 at D 23.0625 from my accepted k_c 135 state there (kc135_d230625/in, blobs a6253940, 49ba2db8)
  kc143_d23125 : k_c 143 at D 23.125 from my accepted k_c 135 state there (kc135_d23125/in, blobs ac01e477, f22d1e21)
Every replacement must occur (an assert); the rung shift 135 -> 143, 127 -> 135, 119 -> 127 of the check names and k_c labels is one regex pass (no cascade). Writes lane_<tag>.sh,
diff_lane.txt (read before use), in/ (copies, blobs checked), in_blobs.txt, push_<name>.sh, summarize_point.py. Read-only on kc135_*; usage: mk_lanes143.py"""
import os, re, shutil, subprocess, sys
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/")
SC = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/953e9688-2a12-485d-a7d9-b760c6e8569c/scratchpad/k143/"


def blob(p):
    return subprocess.check_output(["git", "hash-object", "--no-filters", p]).decode().strip()[:8]


HEADER = """#!/bin/bash
# #1025 macm3 {folder} (t5's order, hc 27 Nov 01:38 UTC by t5's clock): k_c 143 at D {D} by a regrid from my accepted k_c 135 state there (raw I1025-macm3/{srcfolder}/in: state blob {sb}, record blob {rb}; copies in in/).
# Derived from kc135_d23125/lane_d23125.sh by the one-rung shift of the resolutions (119 -> 127, 127 -> 135, 135 -> 143 in the check names and labels) and the explicit replacements of mk_lanes143.py, read in diff_lane.txt.
# Steps: pins, selftests, the new scanner's selftest and its three mutations, the source check (the k_c 135 check accepts the state, controls exit 1 1, the k_c 127 and k_c 143 checks refuse), a wait for no other scan, regrid or secant and
# for 8 GiB available, the regrid ell_refine.py (631e5801, worktree 1025m2 at 48c36355) "{src} 135 {tag} 143 1 {D} {lam0} --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma", the k_c 143 check (blob e15b0ee2, raw 5370db0e3) on the result
# (exit 0, controls 1 1, the k_c 135 check refuses), the NEW scanner (d18_secant.py scan, 92b9bf53, blob eb1396ad) on the lambda plan of scan_plan.env (2 processes), the one-change rule, the secant (tol 1e-5, maxev 10, one process),
# summarize_point.py (the 3-decimal copy, 62c57e1a). Stops (hc to t5): a source or result not accepted (the regrid included), an exception (an array limit included), no robust change or more than one, a step over 8 h, a secant exit other than 0 or 4. usage: bash {lane} [dry|check]
"""

LANES = {
    "A": dict(folder="kc143_d230625", D="23.0625", srcfolder="kc135_d230625", src="l1kc135macm3d230625", tag="l1kc143macm3d230625", sb="a6253940", rb="49ba2db8", lam0="2.0990016035", dn="23.0625_kc143",
              statefile="sol_l1kc135macm3d230625_D23.0625.npy", dt="D23.0625", push="push_kc143_d230625.sh", lane="lane_d230625.sh"),
    "B": dict(folder="kc143_d23125", D="23.125", srcfolder="kc135_d23125", src="l1kc135macm3d23125", tag="l1kc143macm3d23125", sb="ac01e477", rb="f22d1e21", lam0="2.0987860107", dn="23.125_kc143",
              statefile="sol_l1kc135macm3d23125_D23.1250.npy", dt="D23.1250", push="push_kc143_d23125.sh", lane="lane_d23125.sh"),
}


def rep(t, old, new, n=None):
    c = t.count(old)
    assert c >= 1, "not found: %r" % old
    if n is not None:
        assert c == n, "%r occurs %d times, expected %d" % (old, c, n)
    return t.replace(old, new)


def main():
    base = open(R + "kc135_d23125/lane_d23125.sh").read()
    lines = base.split("\n")
    ib0 = lines.index("{"); assert lines[0] == "#!/bin/bash" and ib0 == 6, ib0
    body = "\n".join(lines[ib0:])              # from the opening brace; the old header (lines 0-6) is replaced
    for key in ("A", "B"):
        c = LANES[key]; F = R + c["folder"] + "/"
        os.makedirs(F + "in", exist_ok=True)
        t = body
        # explicit replacements, in this order (each occurs)
        t = rep(t, "kc135_d23125", c["folder"])
        t = rep(t, "push_d23125.sh", c["push"])
        t = rep(t, "exits_kc135.txt", "exits_kc143.txt")
        t = rep(t, "l1kc135macm3d23125", c["tag"])
        t = rep(t, "l1kc127Lmacm3", c["src"])
        t = rep(t, "23.125_kc135", c["dn"])
        t = rep(t, "e1dccb3c", c["sb"])
        if key == "A":
            t = rep(t, "D23.1250", "D23.0625")
            t = rep(t, "LAM0=2.0987860107", "LAM0=2.0990016035")
            t = rep(t, "D=23.125;", "D=23.0625;", 1)
            t = rep(t, "D 23.125", "D 23.0625")
        t = rep(t, "$SRC 127 $TAG 135 1", "$SRC 135 $TAG 143 1", 1)
        t = rep(t, "'^+[^+].*135'", "'^+[^+].*143'", 1)
        t = rep(t, "'^-[^-].*127'", "'^-[^-].*135'", 1)
        t = rep(t, "from 127 to 135", "from 135 to 143", 2)
        t = rep(t, "lane_d23125.sh", c["lane"])
        t = rep(t, "C135", "C143")
        t = rep(t, "C127S", "C135S")
        shift = {"135": "143", "127": "135", "119": "127"}
        t = re.sub(r"(?<!l1)(kc|k_c )(135|127|119)", lambda m: m.group(1) + shift[m.group(2)], t)
        if key == "A":
            assert "23.125" not in t, [l for l in t.split("\n") if "23.125" in l][:3]
        head = HEADER.format(**c)
        out = head + t
        open(F + c["lane"], "w").write(out)
        os.chmod(F + c["lane"], 0o755)
        # the diff against the source lane, to be read
        d = subprocess.run(["diff", R + "kc135_d23125/lane_d23125.sh", F + c["lane"]], capture_output=True, text=True).stdout
        open(F + "diff_lane.txt", "w").write(d)
        # inputs
        chk = R + "kc135_d23125/in/"
        for f in ("kc127_syscheck_1025.py", "kc135_syscheck_1025.py", "read_lower.py", "repeat_check.py", "d18_hybsign.py", "d185_scan_read.py", "capped_run.py", "launch_1070.py"):
            shutil.copy2(chk + f, F + "in/" + f)
        shutil.copy2(SC + "kc143_syscheck_1025.py", F + "in/kc143_syscheck_1025.py")
        sf = R + c["srcfolder"] + "/in/"
        shutil.copy2(sf + c["statefile"], F + "in/" + c["statefile"]); shutil.copy2(sf + c["src"] + ".jsonl", F + "in/" + c["src"] + ".jsonl")
        shutil.copy2(R + "kc135_d23125/summarize_point.py", F + "summarize_point.py")
        ps = open(R + "kc135_d23125/push_d23125.sh").read()
        ps = rep(ps, "kc135_d23125", c["folder"]); ps = rep(ps, "push_d23125.sh", c["push"])
        open(F + c["push"], "w").write(ps)
        ib = ["# blobs (git hash-object --no-filters, first 8) pinned by %s; files under in/ unless a path is given" % c["lane"]]
        for f, want in ((c["statefile"], c["sb"]), (c["src"] + ".jsonl", c["rb"]), ("kc127_syscheck_1025.py", "898ebefa"), ("kc135_syscheck_1025.py", "b353d466"), ("kc143_syscheck_1025.py", "e15b0ee2"),
                        ("read_lower.py", "89309d3c"), ("repeat_check.py", "aaf598a9"), ("d18_hybsign.py", "e089207a"), ("d185_scan_read.py", "7c9d400f"), ("capped_run.py", "11f0647b"), ("launch_1070.py", "56d15f60")):
            got = blob(F + "in/" + f); assert got == want, (f, got, want)
            ib.append("%s in/%s" % (got, f))
        ib.append("%s summarize_point.py" % blob(F + "summarize_point.py")); ib.append("%s %s" % (blob(F + c["push"]), c["push"]))
        open(F + "in_blobs.txt", "w").write("\n".join(ib) + "\n")
        print(key, c["folder"], "lane", c["lane"], "diff lines", d.count("\n"))


if __name__ == "__main__":
    main()
