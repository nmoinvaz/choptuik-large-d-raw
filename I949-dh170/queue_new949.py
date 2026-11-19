#!/usr/bin/env python3
"""#949: queue the states of ks >= 250 that are in the scratch root and not yet named in queue949.txt or queue949_leg08_hold.txt.

    queue_new949.py [--dry]    appends `ks{KS}_D{D:.4f} {path}` to queue949.txt when baseline949.json exists (the baseline is frozen),
                               else to queue949_leg08_hold.txt; prints what it did. KS is read from the path (`_ks250/` for a leg,
                               `/ks260/` for a ladder rung). The states of ks <= 240 are the backfill and are not queued here.
Covers I903-win2/ks_chain (leg08 on), the ladder's bases I903-win2/ks_chain/ladder8/ks*/base_pin*_D*.npz, I903-win2/ks_chain2 and dh370's I966-dh370/ks_chain3."""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.expanduser("~/scratch949")


def names(path):
    return {l.split()[0] for l in open(path) if l.strip()} if os.path.exists(path) else set()


def main():
    frozen = os.path.exists(os.path.join(HERE, "baseline949.json"))
    have = names(os.path.join(HERE, "queue949.txt")) | names(os.path.join(HERE, "queue949_leg08_hold.txt"))
    out = os.path.join(HERE, "queue949.txt" if frozen else "queue949_leg08_hold.txt")
    new = []
    for p in sorted(glob.glob(f"{R}/I903-win2/ks_chain*/**/*.npz", recursive=True) + glob.glob(f"{R}/I966-dh370/ks_chain3*/**/*.npz", recursive=True) + glob.glob(f"{R}/I971-dh610/ks*/base_pin3_D*.npz")):
        rel = os.path.relpath(p, R)
        m, d = re.search(r"[_/]ks(\d+)/", rel), re.search(r"_D(\d+\.\d+)\.npz$", rel)
        if not (m and d) or int(m.group(1)) < 250:
            continue
        pre = "b971_" if "I971-dh610/" in rel else ("c3b_" if "/ks_chain3b/" in rel else ("c3_" if "/ks_chain3/" in rel else ""))   # a name must tell the chains apart (ks 291 is in two)
        name = f"{pre}ks{m.group(1)}_D{d.group(1)}"
        if name not in have:
            its = " --its=32" if float(d.group(1)) > 247.5 else ""    # coordinator, 2026-11-19: --its=32 from D 248 on (sigma_Delta's convergence worsens as sigma_2/sigma_Delta -> 1)
            new.append(f"{name} {rel}{its}")
            have.add(name)
    new.sort(key=lambda l: 0 if "_ks293_D247.28" in l.split()[0] or "D247.28" in l.split()[0] else 1)   # the coordinator's priority read (2026-11-19): ks_chain3b's D 247.28
    for l in new:
        print(("would queue " if "--dry" in sys.argv else ("queued " if frozen else "held ")) + l.split()[0])
    if new and "--dry" not in sys.argv:
        with open(out, "a") as f:
            f.write("".join(l + "\n" for l in new))


main()
