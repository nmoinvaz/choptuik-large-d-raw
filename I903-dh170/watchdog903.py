#!/usr/bin/env python3
"""#903 on dh170: the stop rule of the coordinator's message of 2026-11-17, as a watchdog over chain_k150.log.

    python3 -I watchdog903.py LOG PROCESS_REGEX [--poll 20] [--lam_max 0.03125] [--n 3] [--attempt_s 7200] [--dry]
    python3 -I watchdog903.py --replay LOG [--lam_max ...] [--n ...]
    python3 -I watchdog903.py --selftest [--mutate]

The chain is stopped (its process tree killed, SIGTERM and then SIGKILL after 30 s) when, inside one attempt, the
octo-double Newton's accepted iterations ('on N: ... lam X, dDelta') have lam <= --lam_max for --n in a row, or when
one attempt has run longer than --attempt_s. An attempt starts at its 'a X: re-seeded' line and ends at its
'a X -> D Y' line or an 'attempt refused' line. PROCESS_REGEX is matched by pgrep -f against the chain's command line
and must be anchored with ^ so that this script's own arguments do not match. Events go to watchdog.log beside LOG,
and a stop adds a line to exits_903.txt with the last accepted D, the last base's p_min and the last step's Delta moved.
A log with no new line for --attempt_s is reported (ALERT) and not stopped, since the rule names attempts only.
--selftest runs synthetic cases that must trigger and must not trigger; --mutate shrinks --lam_max to 1e-9, so the
trigger case must then fail and the selftest exits 1."""
import os
import re
import signal
import subprocess
import sys
import time

ATT_START = re.compile(r"^\s+a [0-9.]+: re-seeded")
ATT_END = re.compile(r"^\s+a [0-9.]+ -> D |attempt refused")
ITER = re.compile(r"^\s+on (\d+): .*\blam ([0-9.eE+-]+), dDelta")
ACCEPTED = re.compile(r"^\s+a [0-9.]+ -> D ([0-9.]+):.*moved ([0-9.e+-]+),")
BASE = re.compile(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.")


class Rule:
    def __init__(self, lam_max=1 / 32, n=3, attempt_s=7200):
        self.lam_max, self.n, self.attempt_s = lam_max, n, attempt_s
        self.run, self.t0 = 0, None

    def feed(self, line, now):
        if ATT_START.match(line):
            self.run, self.t0 = 0, now
        elif ATT_END.search(line):
            self.run, self.t0 = 0, None
        else:
            m = ITER.match(line)
            if m:
                self.run = self.run + 1 if float(m.group(2)) <= self.lam_max else 0
                if self.run >= self.n:
                    return f"lam <= {self.lam_max:g} for {self.n} accepted iterations in a row (on {m.group(1)})"
        return None

    def check(self, now):
        if self.t0 is not None and now - self.t0 > self.attempt_s:
            return f"one attempt has run {now - self.t0:.0f} s, past {self.attempt_s} s"
        return None


def selftest(mutate):
    lam_max = 1e-9 if mutate else 1 / 32
    ok = True

    def run(lines, checks=()):
        r = Rule(lam_max=lam_max)
        hit = None
        for t, ln in lines:
            hit = hit or r.feed(ln, t)
        for t in checks:
            hit = hit or r.check(t)
        return hit

    start = (0, "    a 1.0000: re-seeded (ok), 80.0 s")

    def it(k, lam):
        return (1, f"  on {k}: |F| 1e-20 -> 1e-21, |dz| 1e-30 -> 1e-31, lam {lam}, dDelta +1e-31, piv 1e-3..1e+30, 90 s")

    end = (2, "    a 1.000 -> D 231.0: predicted |F| 1e+07, od 4 steps -> 1e+07, moved 1e-17, 300 s")
    cases = [
        ("healthy: lam 1, 0.5, 0.5, 1", [start, it(0, 1), it(1, 0.5), it(2, 0.5), it(3, 1), end], (), False),
        ("crawl: three accepted at 0.0078125", [start, it(0, 1), it(1, 0.0078125), it(2, 0.0078125), it(3, 0.0078125)], (), True),
        ("crawl: exactly 1/32 counts", [start, it(0, 0.03125), it(1, 0.03125), it(2, 0.03125)], (), True),
        ("two crawling, one damped to 0.5, two crawling", [start, it(0, 0.01), it(1, 0.01), it(2, 0.5), it(3, 0.01), it(4, 0.01)], (), False),
        ("two crawling, then a new attempt, one crawling",
         [start, it(0, 0.01), it(1, 0.01), (2, "    a 0.5000: re-seeded (ok), 60.0 s"), it(0, 0.01)], (), False),
        ("lam 0.04 is not <= 1/32", [start, it(0, 0.04), it(1, 0.04), it(2, 0.04)], (), False),
        ("attempt open 7201 s", [start], (7201,), True),
        ("attempt open 7199 s", [start], (7199,), False),
        ("attempt ended, 9000 s later", [start, end], (9000,), False),
    ]
    for name, lines, checks, want in cases:
        got = run(lines, checks) is not None
        flag = "ok" if got == want else "WRONG"
        ok = ok and got == want
        print(f"  {flag:5s} {name}: {'triggers' if got else 'quiet'} (wanted {'trigger' if want else 'quiet'})")
    return ok


def descendants(pid):
    out, todo = [], [pid]
    while todo:
        p = todo.pop()
        kids = subprocess.run(["pgrep", "-P", str(p)], capture_output=True, text=True).stdout.split()
        out += [int(k) for k in kids]
        todo += [int(k) for k in kids]
    return out


def root_pid(regex):
    r = subprocess.run(["pgrep", "-f", regex], capture_output=True, text=True).stdout.split()
    return min(int(p) for p in r) if r else None


def utc():
    return time.strftime("%F %T", time.gmtime())


def summary(log):
    acc, base = None, None
    for ln in open(log, errors="replace"):
        m = ACCEPTED.match(ln)
        if m:
            acc = (m.group(1), m.group(2))
        m = BASE.match(ln)
        if m:
            base = (m.group(2), m.group(3))
    return (f"last accepted D {acc[0]} (Delta moved {acc[1]}), last base D {base[0]} p_min {base[1]}"
            if acc and base else "no accepted step")


def main(argv):
    opt = {"--poll": 20.0, "--lam_max": 1 / 32, "--n": 3, "--attempt_s": 7200.0}
    flags = {"--dry", "--selftest", "--mutate", "--replay"}
    pos, i, on = [], 0, set()
    while i < len(argv):
        if argv[i] in flags:
            on.add(argv[i])
        elif argv[i] in opt:
            opt[argv[i]] = type(opt[argv[i]])(argv[i + 1])
            i += 1
        else:
            pos.append(argv[i])
        i += 1
    if "--selftest" in on:
        print("selftest" + (" (mutated, must FAIL)" if "--mutate" in on else ""))
        ok = selftest("--mutate" in on)
        print("selftest", "passed" if ok else "FAILED")
        return 0 if ok else 1
    rule = Rule(opt["--lam_max"], int(opt["--n"]), opt["--attempt_s"])
    if "--replay" in on:
        hits = 0
        for k, ln in enumerate(open(pos[0], errors="replace"), 1):
            why = rule.feed(ln, 0.0)
            if why:
                hits += 1
                print(f"line {k}: {why}")
        print(f"{hits} trigger(s) in {pos[0]}")
        return 0
    log, regex = pos[0], pos[1]
    here = os.path.dirname(os.path.abspath(log))
    wlog = os.path.join(here, "watchdog.log")

    def say(msg):
        with open(wlog, "a") as f:
            f.write(f"{utc()} UTC {msg}\n")

    f = open(log, errors="replace")
    for ln in f:                                   # the backlog sets the counters, the timer of an open attempt starts now
        rule.feed(ln, time.time())
    say(f"armed on {log}: lam <= {rule.lam_max:g} for {rule.n} in a row, or one attempt past {rule.attempt_s:.0f} s; "
        f"{'dry' if '--dry' in on else 'live'}; attempt {'open' if rule.t0 else 'closed'}, run {rule.run}")
    last_beat, alerted = time.time(), False
    while True:
        why = None
        grew = False
        for ln in f:
            grew = True
            why = why or rule.feed(ln, time.time())
        now = time.time()
        why = why or rule.check(now)
        if grew:
            alerted = False
        elif now - os.path.getmtime(log) > opt["--attempt_s"] and not alerted:
            say(f"ALERT: no new line in {log} for over {opt['--attempt_s']:.0f} s, not stopped (the rule names attempts)")
            alerted = True
        if now - last_beat > 3600:
            say(f"alive, run {rule.run}, attempt {'open' if rule.t0 else 'closed'}")
            last_beat = now
        if why:
            say(f"TRIGGER: {why}")
            if "--dry" in on:
                rule.run, rule.t0 = 0, None
                continue
            pid = root_pid(regex)
            if pid is None:
                say("TRIGGER with no process matching the regex, nothing to kill")
                return 2
            tree = [pid] + descendants(pid)
            say(f"killing the tree of {pid}: {tree}")
            for p in tree:
                try:
                    os.kill(p, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            time.sleep(30)
            left = [p for p in tree if os.path.exists(f"/proc/{p}")]
            for p in left:
                try:
                    os.kill(p, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            time.sleep(2)
            alive = [p for p in tree if os.path.exists(f"/proc/{p}")]
            s = summary(log)
            say(f"killed, SIGKILL needed for {left}, still alive {alive}; {s}")
            with open(os.path.join(here, "exits_903.txt"), "a") as g:
                g.write(f"903 chain_k150 stopped by the watchdog ({why}) at {utc()} UTC; {s}\n")
            return 0
        time.sleep(opt["--poll"])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
