"""Print selected numbers from the four sources (stored, Mac I887, Pi I882, this machine) side by side."""
import json
import os
import re
import subprocess

RW = "C:/Users/nathan/Source/choptuik-large-d-raw-754"
WT = "C:/Users/nathan/Source/choptuik-i893"
SP = "C:/Users/nathan/AppData/Local/Temp/claude/bb1153300f5e1654/458d2fcb-c4f2-4c70-bd54-8689899a03bd/scratchpad"


def stored(name):
    return subprocess.run(["git", "-C", WT, "show", "HEAD:solver/proof/" + name], capture_output=True,
                          encoding="utf-8").stdout


def jload(txt):
    return json.loads(txt)


def get(d, path):
    for p in path:
        d = d[p]
    return d


def row(label, srcs, path):
    out = []
    for nm, d in srcs:
        try:
            out.append(f"{nm} {get(d, path)}")
        except Exception as e:  # noqa
            out.append(f"{nm} -")
    print(label, " | ".join(out))


def rd(p):
    return open(p, encoding="utf-8").read()


for name, paths in [
    ("b5_jump.json", [["CE"], ["xPhi", 0]]),
    ("b5_jump_d0_1e7.json", [["CE"], ["Zc"]]),
    ("b7_ift.json", [["C7"], ["lnC7"], ["ln_n0"], ["rows", 58, 3, 1]]),
]:
    srcs = [("stored", jload(stored(name))), ("mac", jload(rd(f"{RW}/I887-mac/{name}"))),
            ("pi", jload(rd(f"{RW}/I882-rpi5/changed/{name}"))), ("win", jload(rd(f"{RW}/I893-winb/changed/{name}")))]
    for p in paths:
        row(name + " " + "/".join(map(str, p)), srcs, p)

for name, paths in [("b7_box.json", [["state_rad"]]), ("b7_adjoint.json", [["state_rad"], ["chi_rad_rel"]]),
                    ("b7_box_point.json", [["state_rad"]]), ("b7_adjoint_point.json", [["state_rad"], ["chi_rad_rel"]]),
                    ("b7_adjoint_point_mutT.json", [["state_rad"], ["chi_rad_rel"]])]:
    srcs = [("stored", jload(stored(name))), ("pi", jload(rd(f"{RW}/I882-rpi5/changed/{name}"))),
            ("win", jload(rd(f"{RW}/I893-winb/changed/{name}")))]
    for p in paths:
        row(name + " " + "/".join(map(str, p)), srcs, p)

# the first record of the L0 = 62 scan line: iterations, hyp V
def recs(path):
    return [json.loads(l) for l in rd(path).splitlines() if l.strip().startswith("{")]

print("--- scan L0=62 records")
for nm, p in [("stored", None), ("mac", f"{RW}/I887-mac/b8m_scan_K4_box.log"), ("pi", f"{SP}/stagepi/b8m_scan_K4_box.log"),
              ("win", f"{SP}/stage893/b8m_scan_K4_box.log")]:
    rs = [json.loads(l) for l in (stored("b8m_scan_K4_box.log").splitlines() if p is None else rd(p).splitlines())
          if l.strip().startswith("{")]
    r = [x for x in rs if abs(x["L0"] - 62) < 1e-9][-1]
    print(nm, {k: r[k] for k in r if k in ("iters", "closes", "L0", "ratio", "n_iter")}, "hyp.V", r["hyp"]["V"],
          "keys", [k for k in r if "iter" in k or "rel" in k][:4], "last_rel_changes", r.get("last_rel_changes"))

print("--- numcheck jump of the two continuations, line 2")
for nm, p in [("stored", None), ("mac", f"{RW}/I887-mac/b8m_lc_numcheck_n1e3.log"),
              ("pi", f"{RW}/I882-rpi5/b8m_lc_numcheck.log"), ("win", f"{RW}/I893-winb/b8m_lc_numcheck.log")]:
    t = stored("b8m_lc_numcheck_n1e3.log") if p is None else rd(p)
    m = re.search(r"jump of the two continuations at 1 \+ eta: ([0-9.e+-]+)", t)
    print(nm, m.group(1) if m else None)
