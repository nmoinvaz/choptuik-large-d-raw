#!/usr/bin/env python3
"""#949 (coordinator's hc 2026-11-19 ~13:45 UTC, for #966's bar; corrected by the coordinator: dh370's hc cannot reach dh170, so not by hc): after each near_null read of a ks_chain3b
state, post sigma_Delta and sigma_2 (with the Delta shares, the convergence and the state's file) as a short comment on #966, where dh370 reads them for its bar test; the #949 post is separate.
    python relay_dh370_949.py            poll exits_949.txt every 20 s until the deadline (the 48 h stop, 2026-11-19 22:42 UTC); each new `949 c3b_... exit 0` line whose name is not in
                                         sent_dh370.txt is sent once, then recorded there
    python relay_dh370_949.py --send NAME [--force]   send one named read now (the baseline)
    python relay_dh370_949.py --selftest [--mutate|--mutate=sign]   the message of a planted record has the planted numbers, sigma_Delta, sigma_2 and the pinned step's Delta
                                         with its sign (exit 1 if not; --mutate swaps sigma_Delta and sigma_2, --mutate=sign flips the pinned Delta's sign: both must fail)
The state's own sigma_Delta is vector 1 of the JSON when its Delta share is the largest (as track949.py), sigma_2 is the lowest remaining vector that is not the harmonic-3 pair."""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO, ISSUE = "nmoinvaz/choptuik-large-d", "966"      # always --repo: gh in a raw clone resolves the number in the raw repository
SENT = os.path.join(HERE, "sent_dh370.txt")


def deadline_epoch():
    return int(subprocess.run(["date", "-u", "-d", "2026-11-19 22:42:00", "+%s"], capture_output=True, text=True).stdout.strip())


def picks(rec, mutate=False):      # mutate: False, True/"swap" (sigma_Delta and sigma_2 swapped) or "sign" (the pinned Delta's sign flipped, in message())
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and {("p1", 3), ("m_h", 3)} <= {(b, k) for b, k, _ in v[i]["top"]}]
    rest = sorted((i for i in range(len(v)) if i != d and i not in pair), key=lambda i: v[i]["sigma"])
    s2 = rest[0]
    if mutate and mutate != "sign":
        d, s2 = s2, d
    return d, s2


def message(name, rec, mutate=False):
    d, s2 = picks(rec, mutate)
    v = rec["vectors"]
    return (f"dh170 near_null (--k=6 --its=32) of the ks_chain3b state {name}: D {rec['D']:.4f}, state {rec['state']}: sigma_Delta {v[d]['sigma']:.6e} (vector {d + 1}, Delta share {v[d]['delta']:.3f}, "
            f"convergence {v[d]['conv']:.0e}), sigma_2 {v[s2]['sigma']:.6e} (vector {s2 + 1}, Delta share {v[s2]['delta']:.3f}, convergence {v[s2]['conv']:.0e}), sigma_2/sigma_Delta {v[s2]['sigma'] / v[d]['sigma']:.3f}. "
            f"pinned step dz + J^-1 c, its Delta component (the first-order error of Delta, with its sign): {rec['step_pinned']['delta'] * (-1 if mutate == 'sign' else 1):+.3e}. (the same row on #949)")


def send(text):
    for attempt in (1, 2, 3):
        r = subprocess.run(["gh", "issue", "comment", ISSUE, "--repo", REPO, "--body", text], capture_output=True, text=True)
        if r.returncode == 0 and "issuecomment" in r.stdout:
            print("posted", r.stdout.strip(), flush=True)
            return True
        time.sleep(10)
    print("gh comment failed:", r.stdout[-200:], r.stderr[-200:], flush=True)
    return False


def sent_names():
    return {l.split()[0] for l in open(SENT) if l.strip()} if os.path.exists(SENT) else set()


def selftest(mutate):
    rec = dict(D=251.5, state="x/leg05_D250.7060_ks293/anm_pin3_D251.5000.npz", vectors=[
        dict(sigma=2.5e-18, delta=0.74, conv=1e-6, top=[["p1", 1, 0.1]]), dict(sigma=3.0e-18, delta=0.25, conv=2e-6, top=[["p1", 1, 0.1]]),
        dict(sigma=7e-13, delta=0.0, conv=1e-9, top=[["p1", 3, 0.1], ["m_h", 3, 0.1]]), dict(sigma=8e-13, delta=0.0, conv=1e-9, top=[["p1", 3, 0.1], ["m_h", 3, 0.1]]),
        dict(sigma=1e-10, delta=0.0, conv=0.3, top=[["c0", 4, 0.1]]), dict(sigma=2e-10, delta=0.0, conv=0.3, top=[["c0", 4, 0.1]])],
        step_pinned=dict(delta=-4.2e-27))
    m = message("c3b_ks293_D251.5000", rec, mutate)
    ok = ("sigma_Delta 2.500000e-18 (vector 1" in m and "sigma_2 3.000000e-18 (vector 2" in m and "sigma_2/sigma_Delta 1.200" in m
          and "with its sign): -4.200e-27." in m)
    print("selftest" + (f" --mutate={mutate}" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        mut = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), True if "--mutate" in sys.argv else False)
        sys.exit(0 if selftest(mut) else 1)
    if "--send" in sys.argv:
        name = sys.argv[sys.argv.index("--send") + 1]
        rec = json.load(open(os.path.join(HERE, name + ".json")))
        ok = send(message(name, rec))
        if ok:
            open(SENT, "a").write(name + "\n")
        sys.exit(0 if ok else 1)
    end = deadline_epoch()
    done = sent_names()
    pos = os.path.getsize(os.path.join(HERE, "exits_949.txt"))
    print(f"relay started {time.strftime('%F %T', time.gmtime())} UTC, deadline {time.strftime('%F %T', time.gmtime(end))} UTC", flush=True)
    while time.time() < end:
        with open(os.path.join(HERE, "exits_949.txt")) as f:
            f.seek(pos)
            new = f.read()
            pos = f.tell()
        for line in new.splitlines():
            p = line.split()
            if len(p) >= 4 and p[0] == "949" and p[1].startswith("c3b_") and p[2] == "exit" and p[3] == "0" and p[1] not in done:
                try:
                    rec = json.load(open(os.path.join(HERE, p[1] + ".json")))
                except Exception as e:
                    print("cannot read", p[1], e, flush=True)
                    continue
                if send(message(p[1], rec)):
                    open(SENT, "a").write(p[1] + "\n")
                    done.add(p[1])
                    print(time.strftime("%T", time.gmtime()), "sent", p[1], flush=True)
        time.sleep(20)
    print("deadline reached", flush=True)


main()
