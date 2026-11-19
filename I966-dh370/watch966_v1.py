#!/usr/bin/env python3
"""#966 ks_chain3: alert-only watcher of the two conditions the issue says to post on, never stops or kills anything.

    python3 -I watch966.py CHAIN_OUT ALERTS [--poll 20] [--attempt_s 10800] [--refused 3] [--hc]
    python3 -I watch966.py --replay LOG [--attempt_s S] [--refused N]
    python3 -I watch966.py --selftest [--mutate]

CHAIN_OUT is ks_chain3's output directory; the newest leg's anm_run.log is followed. An attempt starts at a 'step N: D' line
or at the end of the attempt before it, and ends at its 'a X -> D' line; it was accepted when 'Delta of the saved state' follows
that line, refused when the next attempt's first line or 'stopped:' does. ALERT lines go to ALERTS (and to the coordinator by hc,
at most every 10 min, with --hc): one attempt running longer than --attempt_s, --refused attempts in a row refused, and a log with no new line for --attempt_s.
--selftest feeds synthetic logs that must and must not alert; --mutate sets both thresholds out of reach, so the cases that must
alert fail and the selftest exits 1."""
import glob
import os
import re
import subprocess
import sys
import time

STEP = re.compile(r"^step \d+: D [0-9.]+,")
START = re.compile(r"^\s+a [0-9.]+: (re-seeded|predicted)")
END = re.compile(r"^\s+a [0-9.]+ -> D ([0-9.]+):")
SAVED = re.compile(r"^\s+Delta of the saved state")
STOP = re.compile(r"^stopped:")


class Rule:
    def __init__(self, attempt_s=10800, refused=3):
        self.attempt_s, self.refused = attempt_s, refused
        self.t0 = None          # start of the running attempt
        self.pending = False    # an 'a X -> D' line is waiting for its verdict
        self.run = 0            # refused attempts in a row
        self.alerted = False    # this attempt's time alert was given

    def _end_pending(self, accepted, now):
        out = []
        if self.pending:
            self.pending = False
            self.run = 0 if accepted else self.run + 1
            if not accepted and self.run == self.refused:
                out.append(f"{self.run} attempts in a row refused")
        return out

    def feed(self, line, now):
        out = []
        if SAVED.match(line):
            out += self._end_pending(True, now)
        elif STEP.match(line):
            out += self._end_pending(True, now)
            self.t0, self.alerted = now, False
        elif START.match(line) or STOP.match(line):
            out += self._end_pending(False, now)
        m = END.match(line)
        if m:
            out += self._end_pending(False, now)
            self.pending = True
            self.t0, self.alerted = now, False      # the next attempt starts here
        return out

    def check(self, now):
        if self.t0 is not None and not self.alerted and now - self.t0 > self.attempt_s:
            self.alerted = True
            return [f"one attempt has run {now - self.t0:.0f} s, past {self.attempt_s} s"]
        return []


def selftest(mutate):
    big = 10 ** 9
    ok = True

    def case(name, lines, want, attempt_s=100, checks=()):
        nonlocal ok
        r = Rule(attempt_s=big if mutate else attempt_s, refused=big if mutate else 3)
        got = []
        for t, ln in lines:
            got += r.feed(ln, t)
        for t in checks:
            got += r.check(t)
        res = bool(got) == want
        print(("ok   " if res else "FAIL ") + name + (f" -> {got}" if got else ""))
        ok &= res

    ref = lambda t, x: [(t, f"    a {x}: re-seeded (ok), 90.0 s"), (t + 1, f"    a {x} -> D 230.5: predicted |F| 1e13, od 3 steps -> 1e13 (tol 1e-20), Delta 1.6")]
    acc = lambda t, x: ref(t, x) + [(t + 2, "      Delta of the saved state, its eight parts summed exactly: 1.6")]
    head = [(0, "step 0: D 229.05, pivots 9e-14..7e39, |z_1| 4e-04")]
    case("three refused in a row alert", head + ref(1, 2) + ref(5, 1) + ref(9, 0.5) + [(13, "    a 0.25: re-seeded (ok), 80 s")], True)
    case("three refused then stopped alert", head + ref(1, 2) + ref(5, 1) + ref(9, 0.5) + [(13, "stopped: no convergence after eight attempts")], True)
    case("two refused then accepted no alert", head + ref(1, 2) + ref(5, 1) + acc(9, 0.5), False)
    case("refused streak reset by an accepted step", head + ref(1, 2) + ref(5, 1) + acc(9, 0.5) + ref(13, 2) + ref(17, 1) + acc(21, 0.5), False)
    case("an attempt past the limit alerts", head, True, attempt_s=100, checks=(50, 150))
    case("an attempt within the limit does not", head, False, attempt_s=100, checks=(50, 99))
    case("a refused attempt's clock restarts", head + ref(1, 2), False, attempt_s=100, checks=(80,))
    return ok


def replay(path, attempt_s, refused):
    r = Rule(attempt_s=attempt_s, refused=refused)
    n = 0
    for i, ln in enumerate(open(path), 1):
        for a in r.feed(ln.rstrip("\n"), i):
            n += 1
            print(f"line {i}: ALERT {a}")
    print(f"{path}: {n} alerts")
    return n


def follow(chain_out, alerts, poll, attempt_s, refused, hc):
    rule, cur, pos, last_hc, silent = Rule(attempt_s, refused), None, 0, 0, False
    while True:
        legs = sorted(glob.glob(os.path.join(chain_out, "leg*", "anm_run.log")), key=os.path.getmtime)
        if legs and legs[-1] != cur:
            cur, pos = legs[-1], 0
            rule = Rule(attempt_s, refused)
        now = time.time()
        msgs = []
        if cur:
            with open(cur) as f:
                f.seek(pos)
                data = f.read()
            nl = data.rfind("\n") + 1          # whole lines only
            pos += nl
            for ln in data[:nl].splitlines():
                msgs += rule.feed(ln, now)
        msgs += rule.check(now)
        if cur and not silent and now - os.path.getmtime(cur) > attempt_s:      # a polish or a step with no log line
            silent = True
            msgs.append(f"log silent for {now - os.path.getmtime(cur):.0f} s")
        elif cur and now - os.path.getmtime(cur) <= attempt_s:
            silent = False
        for m in msgs:
            line = f"{time.strftime('%F %T', time.gmtime())} UTC ALERT {os.path.basename(os.path.dirname(cur or ''))}: {m}"
            with open(alerts, "a") as f:
                f.write(line + "\n")
            if hc and now - last_hc >= 600:
                last_hc = now
                subprocess.run(["hc", "send", "nathans-macbook-air-m5-3/t5", f"dh370 #966 ks_chain3 alert: {m} (watcher only logs, nothing stopped)"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(poll)


def main():
    a = sys.argv[1:]
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    if "--selftest" in a:
        sys.exit(0 if selftest("--mutate" in a) else 1)
    if "--replay" in a:
        replay(a[a.index("--replay") + 1], opt("--attempt_s", 10800), opt("--refused", 3))
        return
    pos = [x for x in a if not x.startswith("--") and not re.fullmatch(r"[0-9]+", x)]
    follow(pos[0], pos[1], opt("--poll", 20), opt("--attempt_s", 10800), opt("--refused", 3), "--hc" in a)


if __name__ == "__main__":
    main()
