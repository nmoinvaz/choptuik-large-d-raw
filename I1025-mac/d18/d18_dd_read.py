"""#1025 D 18 (B): the full dd M's sign against the hybrid's at the same lambda, read under the coordinator's fixed rules
(d18_dd_criteria.log). A dd sign counts if its 5 exact variants agree and 1e-24 relative noise (2 seeds) leaves it unchanged;
a hybrid sign counts if p4_hybrid's 1e-15 noise test leaves it unchanged.
usage: d18_dd_read.py ROOT.jsonl HYBSIGN.jsonl DD.jsonl LAMS | d18_dd_read.py selftest
exit 0: reading (1), dd agrees with the hybrid at every lambda; 2: reading (2), dd disagrees at some lambda; 3: a sign unresolved"""
import sys, json


def hyb_at(root, hs, l):
    for k, v in root["evals"].items():
        if float(k) == l:
            return dict(sign=v["sign"], ln=v["ln"], robust=all(x == v["sign"] for x in v["noise"]), src="root run")
    for r in hs:
        if r["lam"] == l:
            return dict(sign=r["sign"], ln=r["ln"], robust=r["noise_robust"], src="d18_hybsign")
    return None


def dd_at(dds, l):
    r = [x for x in dds if x["lam"] == l and not x.get("mutate")]
    if not r:
        return None
    r = r[-1]; n24 = [e for e in (r["noise"] or []) if e["eps"] == 1e-24]
    return dict(sign=r["dd"][0]["sign"], ln=r["dd"][0]["ln"], agree=r["dd_agree"],
                robust=bool(n24) and all(s == r["dd"][0]["sign"] for s in n24[0]["signs"]), f64=r["f64_sign"])


def read(root, hs, dds, lams):
    rows, code = [], 0
    for l in lams:
        h, d = hyb_at(root, hs, l), dd_at(dds, l)
        ok = h is not None and d is not None and h["robust"] and d["agree"] and d["robust"]
        rows.append((l, h, d, ok))
        if not ok:
            code = 3
        elif h["sign"] != d["sign"] and code != 3:
            code = 2
    return code, rows


if sys.argv[1] == "selftest":                           # planted records: each case must give its reading
    def rt(signs):
        return dict(evals={repr(l): dict(sign=s, ln=-1.0, noise=[s, s]) for l, s in signs})
    def dr(l, s, agree=True, n=None):
        return dict(lam=l, dd=[dict(sign=s, ln=-1.0)] * 5, dd_agree=agree, noise=[dict(eps=1e-24, signs=n or [s, s])], f64_sign=1.0)
    hs = [dict(lam=1.8, sign=-1.0, ln=-1.0, noise_robust=True)]
    cases = [("agree at both", [dr(1.7, 1.0), dr(1.8, -1.0)], 0), ("disagree at one", [dr(1.7, -1.0), dr(1.8, -1.0)], 2),
             ("dd variants split", [dr(1.7, 1.0, agree=False), dr(1.8, -1.0)], 3), ("dd noise flips", [dr(1.7, 1.0), dr(1.8, -1.0, n=[-1.0, 1.0])], 3),
             ("dd missing", [dr(1.7, 1.0)], 3)]
    bad = 0
    for name, dds, want in cases:
        got = read(rt([(1.7, 1.0)]), hs, dds, [1.7, 1.8])[0]; bad += got != want
        print(f"selftest {name}: reading code {got} (want {want}) {'ok' if got == want else 'WRONG'}")
    print("selftest", "passes" if not bad else f"FAILS ({bad})"); sys.exit(1 if bad else 0)
root = [json.loads(l) for l in open(sys.argv[1]) if json.loads(l)["D"] == 18.0][-1]
hs = [json.loads(l) for l in open(sys.argv[2])]
dds = [json.loads(l) for l in open(sys.argv[3])]
lams = [float(v) for v in sys.argv[4].split(",")]
code, rows = read(root, hs, dds, lams)
print("| lambda | hybrid sign | hybrid ln abs det | hybrid noise-robust | dd sign | dd ln abs det | dd 5 variants agree | dd 1e-24 noise unchanged | float64 sign | dd minus hybrid ln |")
print("|---|---|---|---|---|---|---|---|---|---|")
for l, h, d, ok in rows:
    print(f"| {l!r} | {h['sign']:+.0f} | {h['ln']:.10f} | {h['robust']} | {d['sign']:+.0f} | {d['ln']:.10f} | {d['agree']} | {d['robust']} | "
          f"{d['f64']:+.0f} | {d['ln'] - h['ln']:+.2e} |" if h and d else f"| {l!r} | missing | | | | | | | | |")
print({0: "reading (1): dd agrees with the hybrid at every lambda; the hybrid's sign changes are real",
       2: "reading (2): dd disagrees with the hybrid; the hybrid is not trustworthy at D 18",
       3: "no reading: a sign is unresolved or missing"}[code])
sys.exit(code)
