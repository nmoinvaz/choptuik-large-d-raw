#!/usr/bin/env python3
"""#1025 winb, k_c 79 at D 19: looks in raw origin/main (the push worktree, fetched) for win2's k_c 71 D 19 state from its leap (I1025-win2/..., sol_l1kcL71*_D19.0000.npy or _D19.000000.npy)
and its record; when both are there it fetches them with win2's check and the fixed scanner and readers by `git show`, checks every file against its blob (git hash-object --no-filters),
writes prep_kc79d19_pins_1025.txt (blob and raw path per line) and kc79d19_cfg_1025.txt (SRC, SRCSTATE, SRCREC, SRCCHECK), and copies the state into the worktree's data/ under the name
ell_refine.py reads (sol_SRC_D19.0000.npy). Exit 0 found and prepared, 3 not there yet, 1 anything else wrong (more than one candidate tag, a pin mismatch, no D 19 line in the record).
It starts nothing and writes nothing outside this staging folder and the worktree's data/ (never over an existing file)."""
import json, os, re, shutil, subprocess, sys

S = "C:/Users/nathan/Source/kc79d19_1025"
RAWW = "C:/Users/nathan/Source/choptuik-large-d-raw-754"
WTD = "C:/Users/nathan/Source/choptuik-i1025k79/solver/matter/data"
FIXED = [l.split() for l in open(S + "/prep_kc79d19_pins_fixed.txt") if l.strip()]


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", RAWW] + list(a), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr.decode(errors='replace')[:300]}")
    return r.stdout if binary else r.stdout.decode()


def blob_of(path):
    r = subprocess.run(["git", "hash-object", "--no-filters", path], capture_output=True, text=True)
    return r.stdout.strip()


REH = sys.argv[sys.argv.index("--rehearse") + 1] if "--rehearse" in sys.argv else None        # a rehearsal on an existing state, e.g. 18.75: same code, other output files, no copy into the worktree
DV = float(REH) if REH else 19.0
PAT = re.compile(r"^(I1025-win2/.+)/sol_(l1kc71L[A-Za-z0-9]*)_D" + (re.escape(f"{DV:.6f}") if REH else r"19\.0000(00)?") + r"\.npy$")


def pick(tree):
    """returns ('ok', folder, tag, state) | ('none',) | ('many', text) | ('differ', paths) from a {path: blob} map"""
    cand = {}
    for p in tree:
        m = PAT.match(p)
        if m:
            cand.setdefault((m.group(1), m.group(2)), []).append(p)
    if not cand:
        return ("none",)
    if len(cand) > 1:
        return ("many", "; ".join(f"{d} {t}" for d, t in sorted(cand)))
    (folder, tag), paths = next(iter(cand.items()))
    paths.sort()                                         # the .0000 name before the .000000 one
    if len(paths) > 1 and tree[paths[0]] != tree[paths[1]]:
        return ("differ", paths)
    return ("ok", folder, tag, paths[0])


if "--selftest" in sys.argv:
    t0 = {"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D18.750000.npy": "a"}
    t1 = dict(t0, **{"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.000000.npy": "b"})
    t2 = dict(t1, **{"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.0000.npy": "b"})
    t3 = dict(t2, **{"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.0000.npy": "c"})
    t4 = dict(t1, **{"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.0000.npy": "x"})
    cases = [("D 18.75 only", t0, "none"), ("the .6f name only", t1, "ok"), ("both names, equal blobs", t2, "ok"), ("two tags", t3, "many"), ("two names, different blobs", t4, "differ"),
             ("a k_c 63 state at D 19", {"I1025-win2/x/sol_l1kc63Lw1025_D19.0000.npy": "d"}, "none"), ("D 19.5", {"I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.500000.npy": "e"}, "none")]
    ok = True
    for name, t, want in cases:
        got = pick(t)[0]
        print(f"planted: {name}: {got}, expected {want}: {'PASS' if got == want else 'FAIL'}")
        ok = ok and got == want
    print("selftest: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

git("fetch", "-q", "origin")
tree = {}
for ln in git("ls-tree", "-r", "origin/main", "I1025-win2/").splitlines():
    meta, path = ln.split("	", 1)
    tree[path] = meta.split()[2]
r0 = pick(tree)
if r0[0] == "none":
    print("not there yet: no sol_l1kc71L*_D19.0000(00).npy under I1025-win2/ on origin/main")
    sys.exit(3)
if r0[0] == "many":
    print("MORE THAN ONE candidate (folder, tag): " + r0[1] + ": stop, the coordinator rules")
    sys.exit(1)
if r0[0] == "differ":
    print(f"the two D 19 state files differ ({r0[1]}): stop"); sys.exit(1)
_, folder, tag, state = r0
rec = f"{folder}/{tag}.jsonl"
check = f"{folder.rsplit('/', 1)[0] if folder.endswith('/states') else folder}/kc71_syscheck.py"
readme = f"{folder.rsplit('/', 1)[0] if folder.endswith('/states') else folder}/README.md"
for need in (rec, check):
    if need not in tree:
        print(f"not there yet: {need} is missing on origin/main"); sys.exit(3)
want = [(tree[state], state), (tree[rec], rec), (tree[check], check)] + ([(tree[readme], readme)] if readme in tree else [])
pins = [(b, p) for b, p in FIXED] + want
for b, p in pins:
    dst = f"{S}/raw/{p}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(git("show", f"origin/main:{p}", binary=True))
    g = blob_of(dst)
    if g != b:
        print(f"MISMATCH {p}: got {g}, pinned {b}"); sys.exit(1)
    print(f"ok {b} {p}")
lines = [json.loads(x) for x in open(f"{S}/raw/{rec}") if x.strip()]
l19 = [r for r in lines if r.get("D") == DV]
if not l19:
    print(f"not there yet: the record {rec} has no D {DV} line (last D values {[r.get('D') for r in lines][-3:]})"); sys.exit(3)
r = l19[-1]
print(f"record D 19 line: kc {r.get('kc')}, F {r.get('F')}, steps {r.get('steps')}, constraint {r.get('constraint')}, Delta {r.get('Delta')}, h/seconds {r.get('seconds')}")
dst = f"{WTD}/sol_{tag}_D19.0000.npy"
if REH:
    print("rehearsal: no copy into the worktree")
elif os.path.exists(dst):
    if blob_of(dst) != tree[state]:
        print(f"{dst} exists with another blob: stop"); sys.exit(1)
else:
    shutil.copy(f"{S}/raw/{state}", dst)
    if blob_of(dst) != tree[state]:
        print("copy into the worktree differs"); sys.exit(1)
open(S + ("/rehearsal_pins.txt" if REH else "/prep_kc79d19_pins_1025.txt"), "w").write("".join(f"{b} {p}\n" for b, p in pins))
open(S + ("/rehearsal_cfg.txt" if REH else "/kc79d19_cfg_1025.txt"), "w").write(f"SRC={tag}\nSRCSTATE={state}\nSRCREC={rec}\nSRCCHECK={check}\n")
print(f"prepared: SRC {tag}, state {state} (blob {tree[state]}), record {rec} (blob {tree[rec]}), check {check} (blob {tree[check]}); state copied to {dst}")
sys.exit(0)
