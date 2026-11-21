#!/usr/bin/env python3
"""#1057 (coordinator's hc, 21 Nov ~07:20 UTC, amended ~07:30): when a state's classified Delta share in the LOWEST vector reaches 0.9, send that state's file name at once to the coordinator only (he relays it to
dh610 for #1064's ks 315/316 polishes; dh170 has no hc address for dh610) and post the file name as a one-line comment on #1064; dh370 raises ks only after a polish from such a state converges. A share of 0.9 in
another vector past the crossing goes to the coordinator only, with no #1064 comment (#1057's item (e)).

    share_trigger1057.py            watches exits_1057.txt for new `c3b_... exit 0` lines of the lane and checks each state's near_null record (vectors' Delta shares) as soon as the lane ends it
    share_trigger1057.py --selftest [--mutate]    planted records, a stub hc and a stub gh: share exactly 0.9 in v1 sends to the coordinator and comments on #1064, 0.8999 does nothing, 0.95 in v2 sends to the coordinator
                                                  only, a state before the crossing (D <= 260.85, v1 share 0.99) does nothing, a failed first send is retried once and marked a possible duplicate;
                                                  --mutate uses > 0.9 and must fail

States considered: D > 260.85 (the first crossing, D 260.8483), as stopcheck1057.py's item (e). The message carries the state's raw path (the record's `state`), D, the shares and sigmas of the two lowest vectors."""
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE = 0.9
D_CROSS = 260.85
COORD = "nathans-macbook-air-m5-3/t5"
ISSUE = "1064"
REPO = "nmoinvaz/choptuik-large-d"
STRICT = False                                       # --mutate: > 0.9 instead of >= 0.9


def hit(x):
    return x > SHARE if STRICT else x >= SHARE


def decide(rec):
    """-> (targets, text, issue_line or None) or None; issue_line is the one-line #1064 comment (lowest-vector case only). rec: a near_null record (D, state, vectors with delta and sigma)"""
    if rec["D"] <= D_CROSS:
        return None
    v = rec["vectors"]
    k = max(range(len(v)), key=lambda i: v[i]["delta"])
    if not hit(v[k]["delta"]):
        return None
    where = "the LOWEST vector (v1)" if k == 0 else f"vector v{k + 1}, not the lowest"
    line = (f"dh170 #1057: {rec['state']} (D {rec['D']:.4f}): the classified Delta share in the lowest vector is {v[0]['delta']:.4f} (v2 {v[1]['delta']:.4f}); "
            f"sent to the coordinator for #1064's ks 315/316 polishes." if k == 0 else None)
    text = (f"dh170 #1057 share trigger: state {rec['state']} (D {rec['D']:.4f}): the classified Delta share is {v[k]['delta']:.4f} in {where} "
            f"(v1 share {v[0]['delta']:.4f} sigma {v[0]['sigma']:.4e}, v2 share {v[1]['delta']:.4f} sigma {v[1]['sigma']:.4e}). "
            f"File: {rec['state']} (raw origin/main, dh370's ks_chain3b). Record I1057-dh170/{os.path.basename(rec.get('_name', ''))}.")
    return [COORD], text, line


def send(hcsend, target, text, log):
    for attempt in (1, 2):
        t = text if attempt == 1 else text + " (retry: possible duplicate)"
        r = subprocess.run(hcsend + [target, t], capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip().replace("\n", " ")[:200]
        ok = r.returncode == 0 and '"status":"done"' in out.replace(" ", "")
        log(f"send to {target} attempt {attempt}: {'ok' if ok else 'FAILED'}: {out}")
        if ok:
            return True
        time.sleep(0 if "--selftest" in sys.argv else 20)
    return False


def comment(ghcmd, line, log):
    for attempt in (1, 2):
        r = subprocess.run(ghcmd + [ISSUE, "--repo", REPO, "--body", line], capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip().replace("\n", " ")[:200]
        log(f"#{ISSUE} comment attempt {attempt}: {'ok' if r.returncode == 0 else 'FAILED'}: {out}")
        if r.returncode == 0:
            return True
        time.sleep(0 if "--selftest" in sys.argv else 20)
    return False


def selftest(mutate):
    global STRICT, HERE
    STRICT = mutate
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        stub = os.path.join(tmp, "hcstub.sh")
        open(stub, "w").write('#!/bin/bash\nf=$(dirname $0)/count_${1//\\//_}; n=$(cat $f 2>/dev/null || echo 0); echo $((n+1)) > $f\n'
                              'echo "$1" >> $(dirname $0)/sent.txt\n[ "$1" = "nathans-macbook-air-m5-3/t5" ] && [ $n = 0 ] && { echo \'{"error":"stub failure"}\'; exit 4; }\necho \'{"started":true,"status":"done","turn":1}\'\n')
        os.chmod(stub, 0o755)
        ghstub = os.path.join(tmp, "ghstub.sh")
        open(ghstub, "w").write('#!/bin/bash\necho "$@" >> $(dirname $0)/gh_calls.txt\n')
        os.chmod(ghstub, 0o755)

        def rec(D, s1, s2, name="c3b_test"):
            return {"D": D, "state": f"I966-dh370/ks_chain3b/leg99_test/anm_pin3_D{D:.4f}.npz", "_name": name + ".json",
                    "vectors": [{"delta": s1, "sigma": 1e-20}, {"delta": s2, "sigma": 2e-20}, {"delta": 0.001, "sigma": 1e-14}]}
        cases = [("v1 share exactly 0.9 past the crossing", rec(261.5, 0.9, 0.09), ([COORD], True)),
                 ("v1 share 0.8999", rec(261.5, 0.8999, 0.1), None),
                 ("v2 share 0.95 (coordinator only, no #1064 comment)", rec(261.5, 0.04, 0.95), ([COORD], False)),
                 ("a state before the crossing with v1 share 0.99", rec(260.0073, 0.99, 0.001), None),
                 ("the crossing state itself, D 260.8483, share 0.498", rec(260.8483, 0.498, 0.494), None)]
        for label, r, want in cases:
            got = decide(r)
            g = (got[0], got[2] is not None) if got else None
            good = g == want
            ok &= good
            print(f"selftest: {label}: (targets, #1064 line) {g} (want {want}): {'pass' if good else 'FAIL'}")
        logs = []
        got = decide(cases[0][1])
        if got:
            for tg in got[0]:
                send([stub], tg, got[1], logs.append)
            if got[2]:
                comment([ghstub, "issue", "comment"], got[2], logs.append)
        sent = open(os.path.join(tmp, "sent.txt")).read().split() if os.path.exists(os.path.join(tmp, "sent.txt")) else []
        calls = open(os.path.join(tmp, "gh_calls.txt")).read().splitlines() if os.path.exists(os.path.join(tmp, "gh_calls.txt")) else []
        good = sent == [COORD, COORD] and any("attempt 2: ok" in x for x in logs)
        ok &= good
        print(f"selftest: stub hc sends {sent} (want the coordinator twice: the first send fails and is retried once, marked as a possible duplicate): {'pass' if good else 'FAIL'}")
        good = len(calls) == 1 and "1064" in calls[0] and "--repo nmoinvaz/choptuik-large-d" in calls[0] and "anm_pin3_D261.5000.npz" in calls[0] and "\n" not in calls[0]
        ok &= good
        print(f"selftest: stub gh calls {len(calls)} (want one #1064 comment naming the file on one line): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    logf = os.path.join(HERE, "share_trigger1057.log")

    def log(m):
        with open(logf, "a") as f:
            f.write(f"{time.strftime('%F %T', time.gmtime())} UTC {m}\n")
    ex = os.path.join(HERE, "exits_1057.txt")
    pos = sum(1 for _ in open(ex))
    log(f"start, watching {ex} from line {pos + 1}; share {'>' if STRICT else '>='} {SHARE} past D {D_CROSS}")
    hcsend = os.environ.get("T1057_HCSEND", "hc send --json").split()
    seen = set()
    while not os.path.exists(os.path.join(HERE, "STOP1057")):
        lines = open(ex).read().splitlines()
        for ln in lines[pos:]:
            w = ln.split()
            if len(w) > 3 and w[0] == "1057" and w[1].startswith("c3b_") and w[2] == "exit" and w[3] == "0" and w[1] not in seen:
                seen.add(w[1])
                p = os.path.join(HERE, w[1] + ".json")
                try:
                    rec = json.load(open(p)); rec["_name"] = os.path.basename(p)
                except Exception as e:
                    log(f"{w[1]}: record unreadable: {e}")
                    continue
                v = rec["vectors"]
                log(f"{w[1]}: D {rec['D']:.4f}, shares v1 {v[0]['delta']:.4f} v2 {v[1]['delta']:.4f}")
                d = decide(rec)
                if d:
                    log(f"{w[1]}: TRIGGER, sending to {d[0]}" + (f" and commenting on #{ISSUE}" if d[2] else ""))
                    for tg in d[0]:
                        send(hcsend, tg, d[1], log)
                    if d[2]:
                        comment(os.environ.get("T1057_GHCMD", "gh issue comment").split(), d[2], log)
        pos = len(lines)
        time.sleep(10)
    log("STOP1057 seen, end")


if __name__ == "__main__":
    STRICT = "--mutate" in sys.argv
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest(STRICT) else 1)
    main()
