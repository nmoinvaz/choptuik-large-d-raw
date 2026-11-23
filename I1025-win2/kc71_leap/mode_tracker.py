#!/usr/bin/env python3
"""mode_tracker.py: the fold reading of #1025's k_c 71 / k_c 79 legs past D 20.75 (the coordinator's ruling, hc 2026-11-23 ~21:00 UTC).

The written-before criterion "k_c 79 sigma_reg stays above leg 4's" fails as written from D 20.875: sigma_reg = sv_reg_small[0] is the
smallest singular value above the null cutoff 1e-12 sigma_max, so it jumps when a mode ENTERS (n_null falls; k_c 71 at D 20.75, k_c 79 at
D 20.875) or LEAVES (n_null rises). Replacement, fixed for every later point of both legs: a fold signature is
  (i)  a regular mode's singular value, tracked by identity across points (entries included once tracked), falling at 3 consecutive
       points while its tangent |cos| rises above 0.3, or
  (ii) dDelta/dD changing sign.
Identity across two consecutive points comes from the four-value lists sv_reg_small and the change dn of n_null (records of ell_leap.py):
  dn = 0: new[i] <- old[i];  dn = -1 (a mode entered from below the cutoff): new[0] is new, new[i] <- old[i-1];
  dn = +1 (the weakest mode sank below the cutoff): new[i] <- old[i+1] (i = 0..2), new[3] is new;  |dn| >= 2: all new.
A mode is "tracked" at a point when it has a predecessor. Per row: D, dDelta/dD, the tracked weak mode (the smallest sigma among tracked
modes: id, sigma, ratio to its previous sigma), the mode with the largest tangent |cos| (id or new, sigma, cos), the longest run of
consecutive falls with its cos, and the signature (none, (i), (ii)).
usage: mode_tracker.py RECORDS1.jsonl [RECORDS2.jsonl ...] [--from D]   (the files in chain order; rows from D on, default all after the first)
       mode_tracker.py --selftest [--mutate=count|cos|entry]   (exit 0 only if every planted case reads as written)"""
import json
import sys

FALLS = 3
COS_BAR = 0.3


def link(old_n, new_n, nold, nnew, mutate=None):
    """index in the old list for each of the 4 new entries (None = new mode)."""
    dn = nnew - nold
    if mutate == "entry":
        dn = 0 if dn == -1 else dn
    if dn == 0:
        return [0, 1, 2, 3]
    if dn == -1:
        return [None, 0, 1, 2]
    if dn == 1:
        return [1, 2, 3, None]
    return [None] * 4


def track(recs, mutate=None):
    """rows for recs[1:]; each record needs D, Delta, n_null, sv_reg_small, cos_t_reg."""
    falls_need = 2 if mutate == "count" else FALLS
    ids = list(range(4))
    nxt = 4
    falls = {i: 0 for i in ids}
    rows = []
    prev_slope = None
    for k in range(1, len(recs)):
        a, b = recs[k - 1], recs[k]
        m = link(a["sv_reg_small"], b["sv_reg_small"], a["n_null"], b["n_null"], mutate)
        nid, nfalls, ratio = [], {}, {}
        for i, j in enumerate(m):
            if j is None:
                nid.append(nxt)
                nfalls[nxt] = 0
                nxt += 1
            else:
                t = ids[j]
                nid.append(t)
                r = b["sv_reg_small"][i] / a["sv_reg_small"][j]
                ratio[t] = r
                nfalls[t] = falls.get(t, 0) + 1 if r < 1 else 0
        slope = (b["Delta"] - a["Delta"]) / (b["D"] - a["D"])
        cos = b["cos_t_reg"]
        tracked = [i for i, j in enumerate(m) if j is not None]
        w = min(tracked, key=lambda i: b["sv_reg_small"][i]) if tracked else None
        c = max(range(4), key=lambda i: cos[i])
        sig_i = [i for i in tracked if nfalls[nid[i]] >= falls_need and (mutate == "cos" or cos[i] > COS_BAR)]
        sig_ii = prev_slope is not None and (slope == 0.0 or (slope > 0) != (prev_slope > 0))
        sig = [s for s, on in (("(i)", bool(sig_i)), ("(ii)", sig_ii)) if on]
        longest = max((nfalls[nid[i]], i) for i in tracked)[1] if tracked else None
        rows.append(dict(D=b["D"], slope=slope, n_null=b["n_null"], weak=None if w is None else (nid[w], b["sv_reg_small"][w], ratio[nid[w]]),
                         big=(nid[c] if m[c] is not None else "new", b["sv_reg_small"][c], cos[c]),
                         run=None if longest is None else (nfalls[nid[longest]], cos[longest], nid[longest], b["sv_reg_small"][longest]), sig=sig or ["none"], entered=[nid[i] for i, j in enumerate(m) if j is None]))
        ids, falls, prev_slope = nid, nfalls, slope
    return rows


def fmt(r):
    w = "-" if r["weak"] is None else "m%d %.3e (x%.3f)" % r["weak"]
    big = "%s %.3e cos %.4f" % (("m%d" % r["big"][0]) if r["big"][0] != "new" else "new", r["big"][1], r["big"][2])
    run = "-" if r["run"] is None else "%d falls (m%d %.3e), cos %.3f" % (r["run"][0], r["run"][2], r["run"][3], r["run"][1])
    ent = ("entered " + ",".join("m%d" % e for e in r["entered"])) if r["entered"] else ""
    return "| %.8g | %+.6f | %d | %s | %s | %s | %s | %s |" % (r["D"], r["slope"], r["n_null"], w, big, run, "/".join(r["sig"]), ent)


def _rec(D, Delta, n_null, sv, cos):
    return dict(D=D, Delta=Delta, n_null=n_null, sv_reg_small=sv, cos_t_reg=cos)


def selftest(mutate=None):
    bad = []
    e = 1e-11
    # 1: an entry: n_null 64 -> 63, the new smallest value has no predecessor, the weak TRACKED mode is the old smallest, no signature
    r = track([_rec(1.0, 1.0, 64, [4 * e, 15 * e, 26 * e, 28 * e], [.01] * 4), _rec(1.03, 1.03, 63, [1.4 * e, 4.4 * e, 16 * e, 29 * e], [.05, .01, .01, .01])], mutate)[0]
    if not (r["entered"] and r["weak"] is not None and abs(r["weak"][1] - 4.4 * e) < 1e-20 and r["weak"][0] == 0 and r["sig"] == ["none"]):
        bad.append("entry: %s" % r)
    # 2: three consecutive falls with the cos reaching 0.35: flagged at the third fall, not at the second
    sv = [5, 4.5, 4.0, 3.5]
    cs = [.1, .2, .28, .35]
    chain = [_rec(1 + .03 * i, 1 + .03 * i, 63, [s * e, 9 * e, 20 * e, 30 * e], [c, .01, .01, .01]) for i, (s, c) in enumerate(zip(sv, cs))]
    rows = track(chain, mutate)
    got = [x["sig"] for x in rows]
    if got != [["none"], ["none"], ["(i)"]]:
        bad.append("three falls with cos 0.35: %s, want none, none, (i)" % got)
    # 3: three falls with the cos staying at 0.2: no signature
    chain = [_rec(1 + .03 * i, 1 + .03 * i, 63, [s * e, 9 * e, 20 * e, 30 * e], [.2, .01, .01, .01]) for i, s in enumerate(sv)]
    got = [x["sig"] for x in track(chain, mutate)]
    if got != [["none"]] * 3:
        bad.append("three falls with cos 0.2: %s, want none" % got)
    # 4: two falls then a rise with cos 0.4: no signature (the run resets)
    sv4 = [5, 4.5, 4.0, 4.4]
    chain = [_rec(1 + .03 * i, 1 + .03 * i, 63, [s * e, 9 * e, 20 * e, 30 * e], [.4, .01, .01, .01]) for i, s in enumerate(sv4)]
    got = [x["sig"] for x in track(chain, mutate)]
    if mutate != "cos" and got != [["none"]] * 3:
        bad.append("two falls then a rise: %s, want none" % got)
    # 5: dDelta/dD changes sign: (ii)
    chain = [_rec(1.0, 1.0, 63, [5 * e, 9 * e, 20 * e, 30 * e], [.01] * 4), _rec(1.03, 1.03, 63, [5.2 * e, 9.2 * e, 20 * e, 30 * e], [.01] * 4),
             _rec(1.06, 1.029, 63, [5.4 * e, 9.4 * e, 20 * e, 30 * e], [.01] * 4)]
    got = [x["sig"] for x in track(chain, mutate)]
    if got != [["none"], ["(ii)"]]:
        bad.append("slope turns: %s, want none, (ii)" % got)
    # 6: a mode sinks below the cutoff (n_null +1): the lists shift the other way, the last entry is new
    r = track([_rec(1.0, 1.0, 63, [2 * e, 5 * e, 16 * e, 29 * e], [.01] * 4), _rec(1.03, 1.03, 64, [5.1 * e, 16.2 * e, 29.5 * e, 35 * e], [.01] * 4)], mutate)[0]
    if not (r["entered"] == [4] or len(r["entered"]) == 1) or r["weak"] is None or abs(r["weak"][2] - 5.1 / 5) > 1e-9:
        bad.append("exit: %s" % r)
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s%s" % ("FAILS" if bad else "passes", " (mutate=%s)" % mutate if mutate else ""))
    return 1 if bad else 0


def main():
    a = sys.argv[1:]
    mutate = next((x.split("=", 1)[1] for x in a if x.startswith("--mutate=")), None)
    if "--selftest" in a:
        sys.exit(selftest(mutate))
    start = float(a[a.index("--from") + 1]) if "--from" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and not (i > 0 and a[i - 1] == "--from")]
    recs = []
    for f in files:
        recs += [json.loads(l) for l in open(f) if l.strip()]
    seen, chain = set(), []
    for r in recs:
        key = round(r["D"], 6)
        if key not in seen:
            seen.add(key)
            chain.append(r)
    chain.sort(key=lambda r: r["D"])
    print("| D | dDelta/dD | n_null | tracked weak mode: sigma (x prev) | largest-cos mode: sigma, cos | longest fall run, its cos | signature | entry |")
    print("|---|---|---|---|---|---|---|---|")
    for r in track(chain):
        if start is None or r["D"] >= start - 1e-9:
            print(fmt(r))


if __name__ == "__main__":
    main()
