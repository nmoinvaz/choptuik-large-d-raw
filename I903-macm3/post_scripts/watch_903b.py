"""macm3b #903: wake on a stop, a Traceback, a non-converged step, more than two attempts or an a below 0.15
(refusals at a = 1 and 0.625 are already posted), a D milestone, or the fold rule's exit 0 (stop) or 1 (control failed);
else after 180 minutes. After each new jet with base D >= 258.5 it runs the coordinator's command, hp/fold_est_903.py
verdict at main 3c1b9582 with --ref_Dstar=259.90361142 --ref_err=5.3e-4, and keeps its output in I903-macm3/fold_verdict_k135.log and fold_verdict.json."""
import json, os, re, subprocess, sys, time, datetime
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I903-macm3")
RAW = os.path.expanduser("~/Source/choptuik-large-d-raw-903")
HP = os.path.expanduser("~/Source/choptuik-large-d-903f/hp")
PY = "/Users/nathan/Source/venv-macm3-main/bin/python3"
MILESTONES = [259.0]
FOLD_FROM = 258.5
def recs():
    try: return [json.loads(l) for l in open(f"{O}/chain_k135b/anm_run.jsonl")]
    except Exception: return []
def alive():
    return subprocess.run(["pgrep", "-f", "anm_run.py.*chain_k135b"], capture_output=True).returncode == 0
def saved_jets():
    s = {}
    for l in open(f"{O}/chain_k135b.log"):
        m = re.search(r"the series saved as \S*jet_pin3_D([0-9.]+)\.npz", l)
        if m: s[m.group(1)] = float(m.group(1))
    return s
def run_fold(tag):
    t0 = time.time()
    with open(f"{O}/fold_verdict_k135.log", "a") as f:
        f.write(f"=== verdict run after jet D {tag}, {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n"); f.flush()
        p = subprocess.run(["caffeinate", "-is", "nice", "-n", "10", PY, "-u", "fold_est_903.py", "verdict", f"{O}/chain_k135b", RAW, "--ref_Dstar=259.90361142", "--ref_err=5.3e-4",
                            f"--json={O}/fold_verdict.json"], cwd=HP, stdout=f, stderr=subprocess.STDOUT)
        f.write(f"=== exit {p.returncode}, {time.time()-t0:.0f} s\n")
    with open(f"{O}/exits_k135.txt", "a") as f:
        f.write(f"903m fold verdict after jet D {tag} exit {p.returncode} wall {time.time()-t0:.0f} s {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    return p.returncode
r0 = recs(); n0 = len(r0)
D0 = r0[-1]["attempts"][-1]["D"] if r0 else 0.0
passed = [m for m in MILESTONES if D0 >= m]
seen = set(saved_jets())
t0 = time.time(); why = "180 minutes passed"
while time.time() - t0 < 180 * 60:
    time.sleep(30)
    if not alive(): why = "anm_run is not running"; break
    if "Traceback" in open(f"{O}/chain_k135b.log").read(): why = "a Traceback in the log"; break
    stop = False
    for tag, d in sorted(saved_jets().items(), key=lambda kv: kv[1]):
        if tag in seen: continue
        seen.add(tag)
        if d >= FOLD_FROM:
            code = run_fold(tag)
            if code == 0: why = f"fold rule exit 0 (STOP) after jet D {tag}"; stop = True; break
            if code == 1: why = f"fold rule exit 1 (control 1 failed) after jet D {tag}"; stop = True; break
            if code != 2: why = f"fold rule exit {code} (unexpected) after jet D {tag}"; stop = True; break
            if code == 2: why = f"fold rule exit 2 (continue) after jet D {tag}, report its base lines"; stop = True; break
    if stop: break
    r = recs()
    for x in r[n0:]:
        a = x["attempts"]
        if not x["converged"] or len(a) > 3 or a[-1]["a"] < 0.1:
            why = f"step {x['step'] + 49}: converged {x['converged']}, {len(a)} attempts, a {a[-1]['a']}"; break
    else:
        if r and len(r) == 1 and n0 == 0:
            why = "first accepted step of the --qd_it 40 restart"; break
        if r:
            D = r[-1]["attempts"][-1]["D"]
            new = [m for m in MILESTONES if D >= m and m not in passed]
            if new: why = f"D {D:.5f} passed {new[0]:.0f}"; break
        continue
    break
print(f"wake at {datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC: {why}; records {len(recs())}")
