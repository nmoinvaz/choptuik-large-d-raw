import json, re, subprocess, datetime, sys
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
rc = sys.argv[1] if len(sys.argv) > 1 else "RAWCOMMIT"
ex = open(f"{O}/exits_k135.txt").read().splitlines()
stop = next(x for x in ex if "chain_k135 exit" in x)
st = next(x for x in ex if "chain_k135b start" in x)
m = re.search(r"exit (\d+) wall (\d+)s (\S+ \S+ UTC)", stop); ecode, ewall, etime = m.groups()
stime = re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)", st).group(1)
a = [json.loads(l) for l in open(f"{O}/chain_k135/anm_run.jsonl")]
last = a[-1]
La = open(f"{O}/chain_k135.log").read().splitlines()
Lb = open(f"{O}/chain_k135b.log").read().splitlines()
# the old chain's last lines: no attempt of step 49 had started
tail_a = [l for l in La[-3:]]
i_end = max(i for i, l in enumerate(La) if re.match(r"\s+a [0-9.]+ -> D ", l))
started49 = any(re.match(r"\s+a [0-9.]+: re-seeded", l) for l in La[i_end:])
ser48 = re.search(r", (\d+) s$", next(l for l in La if l.startswith("step 48: D "))).group(1)
fa = re.search(r'^F="(.*)"$', open(f"{O}/run_903_k135.sh").read(), re.M).group(1).split()
fb = re.search(r'^F="(.*)"$', open(f"{O}/run_903_k135b.sh").read(), re.M).group(1).split()
diff = [(fa[i - 1] + " " + x, fb[i - 1] + " " + y) for i, (x, y) in enumerate(zip(fa, fb)) if x != y]
assert len(fa) == len(fb)
pol = next((l.strip() for l in Lb if re.match(r"\s+on 0: \|F\| \S+ converged", l)), None)
base = next((l for l in Lb if l.startswith("base ")), None)
dsaved = next(l for l in reversed(La) if "Delta of the saved state" in l).split(": ")[1][:20]
print(f"## #903 macm3b: restart with `--qd_it 40`, the cap alone changed, from the base at D {last['attempts'][-1]['D']:.8f} ({datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M UTC')})\n")
print("The coordinator's decision (hc): raise `--qd_it` from 20 to 40 when the current attempt ends, accepted or refused, restart from the last accepted base with every other flag unchanged, and do not kill a running attempt. The hc reached me when the chain was between two attempts, forming the series at step 49's base, so I restarted at once from that base instead of letting step 49's first attempt run under the cap of 20 (the series is formed again by the restart, step 48's took " + ser48 + " s).\n")
print("| | |\n|---|---|")
print(f"| old chain `chain_k135` | stopped by SIGTERM at {etime} (exit {ecode}, wall {ewall} s), during the series at its base of step 49, after step 48's accepted attempt and before step 49's first attempt had started ({'one had started' if started49 else 'none had started'} in the log), so no attempt was killed |")
print(f"| last accepted base | step {last['step']} of `chain_k135`, `chain_k135/anm_pin3_D{last['attempts'][-1]['D']:.4f}.npz`, D {last['attempts'][-1]['D']:.9f}, a {last['attempts'][-1]['a']!r}, accepted at its first attempt ({len(last['attempts'])} attempt), Delta {dsaved} |")
print(f"| restart | `run_903_k135b.sh` at {stime}, into `chain_k135b/` and `chain_k135b.log`, same code (main 5897ee28, the 1f3cda09 hpkernel), 6 threads, nice 10 under caffeinate |")
print(f"| flag differences from `run_903_k135.sh`'s `F` | " + "; ".join(f"`{x}` becomes `{y}`" for x, y in diff) + ", and no other flag of `F` differs |")
print("| added | `--a0 0.14901161193847656` = 1.25 x 0.11920928955078125, the a the chain would have tried next (`--a_grow 1.25`, `--a_hold 1`, step 48 accepted at its first attempt); a restart without it starts at `--h_max` 1.0 |")
print("| unchanged | `--ks 135 --keep_plan 1 --steps 400 --D_max 262`, the state's own plan (21 steps) and the held fit |")
print("")
if pol: print(f"The restart's base polish: `{pol}`.\n")
if base: print(f"The base line: `{base[:260]}`.\n")
print("From here the chain's records are in `chain_k135b/anm_run.jsonl` (its step 0 is the chain's step 49) and its jets, including the ones the fold rule reads (base D of at least 258.5), are in `chain_k135b/`; the fold rule's command is run on `chain_k135b`, everything else in it as the coordinator gave it. Each later post gives the corrections per accepted step and the a, with the cap, in its table.\n")
print(f"Raw: `I903-macm3/` at commit `{rc}` of choptuik-large-d-raw.")
