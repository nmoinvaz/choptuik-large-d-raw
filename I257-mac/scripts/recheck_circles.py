"""#257: the circles of hp/modecount_circle.py re-run from their evaluation caches, with the old rule and with the
alias rule of #242 (hp/modecount_circle.py of wip/i254, b40fa99), no new determinants.

    python3 recheck_circles.py CODE_HP_DIR OUT.jsonl RECORDS.jsonl CACHE.jsonl [CACHE ...]

For each record of RECORDS, every CACHE whose name holds its tag (modecount_<tag>_evals.jsonl) is tried: (1) circle()
with --mutate=flat, the old rule, from that cache, at n0 = the record's (zeros_n), 16, 20, 24; its points, winding and
largest step must equal the record's (the replay control: the record's samples are in that cache). A record that no
cache reproduces is reported as such. (2) circle() with the alias rule from the reproducing cache. A point the rule
needs that the cache lacks stops the replay: the verdict is then "needs new determinants", with that first point;
otherwise the winding is compared with the record's. Exit 1 if a record is not reproduced.
"""
import json
import math
import os
import sys

sys.path.insert(0, sys.argv[1])
import modecount_circle as C  # noqa: E402


class Missing(Exception):
    pass


def cache_of(path):
    v = {}
    for line in open(path):
        r = json.loads(line)
        v[(r["re"], r["im"])] = (r["lnabs"], r["arg"])
    return v


def det_from(v):
    def det(lam):
        k = (float(lam.real), float(lam.imag))
        if k not in v:
            raise Missing(k)
        return v[k]
    return det


out = open(sys.argv[2], "a")
rp = sys.argv[3]
caches = {cp: cache_of(cp) for cp in sys.argv[4:]}
bad = 0
for line in open(rp):
    rec = json.loads(line)
    tag = rec.get("tag")
    c, R = complex(*rec["center"]), rec["R"]
    res = dict(records=rp, tag=tag, center=rec["center"], R=R, record_winding=rec["winding"],
               record_points=rec["points"], record_max_step=rec["max_step"])
    found = None
    for cp, v in caches.items():
        if os.path.basename(cp) != f"modecount_{tag}_evals.jsonl":
            continue
        for n in dict.fromkeys([rec.get("zeros_n", 16), 16, 20, 24]):
            try:
                old = C.circle(det_from(v), c, R, math.pi / 4, n, "flat")
            except Missing:
                continue
            if (old["points"] == rec["points"] and abs(old["winding"] - rec["winding"]) < 1e-9
                    and abs(old["max_step"] - rec["max_step"]) < 1e-9):
                found = (cp, n)
                break
        if found:
            break
    if not found:
        bad += 1
        res.update(replay_ok=False, verdict="record not reproduced by any given cache")
        print(f"{tag} c {c.real:+.4f}{c.imag:+.4f}i R {R}: record winding {rec['winding']:+.4f} ({rec['points']} "
              f"points): NOT REPRODUCED by any given cache", flush=True)
        out.write(json.dumps(res) + "\n")
        continue
    cp, n = found
    res.update(replay_ok=True, cache=cp, n0=n)
    try:
        new = C.circle(det_from(caches[cp]), c, R, math.pi / 4, n)
        res.update(new_points=new["points"], new_winding=new["winding"], new_max_step=new["max_step"],
                   alias_bisections=new["alias_bisections"], max_scale_h=new["max_scale_h"], resolved=new["resolved"],
                   verdict="unchanged" if abs(new["winding"] - rec["winding"]) < 1e-9 else "CHANGED")
        txt = (f"alias rule: {new['points']} points, winding {new['winding']:+.4f}, bisections "
               f"{new['alias_bisections']}, largest arc*scale {new['max_scale_h']:.2f}, resolved {new['resolved']}")
    except Missing as e:
        res.update(verdict="needs new determinants", first_missing=list(e.args[0]))
        txt = f"alias rule needs a determinant not in the cache, first at {e.args[0][0]:.6f} {e.args[0][1]:+.6f}i"
    print(f"{tag} c {c.real:+.4f}{c.imag:+.4f}i R {R}: record winding {rec['winding']:+.4f} ({rec['points']} points), "
          f"replayed from {os.path.basename(os.path.dirname(cp))} (n0 {n}); {txt} -> {res['verdict']}", flush=True)
    out.write(json.dumps(res) + "\n")
print(f"records not reproduced: {bad}")
sys.exit(1 if bad else 0)
