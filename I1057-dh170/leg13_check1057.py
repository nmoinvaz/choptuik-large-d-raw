#!/usr/bin/env python3
"""#1057 (coordinator's hc 2026-11-20 23:3x UTC): dh370 runs leg 13 (I966-dh370/ks_chain3b/leg13_D260.8483_ks293, --od_accept own) after stopping leg 12.
Does the reader already take its states? The three places that name a state's folder are checked on planted paths, with the real code:

    leg13_check1057.py [--mutate]

1. sync949.sh's grep pattern (read from the script) copies `.../leg13_D260.8483_ks293/anm_pin3_D261.0123.npz` and not leg 12's jet_pin3/pred_pin3 files.
2. queue_new949.py --dry (HOME pointed at a temp tree with that file in a scratch949) would queue `c3b_ks293_D261.0123`, and nothing for a state whose name is
   already queued (anm_pin3_D260.6706.npz in a leg 13 folder).
3. stopcheck1057.pushed_unread lists c3b_ks293_D261.0123 as unread and not the jet/pred files.
Control: --mutate plants the same state in a folder of a chain the reader does not cover (ks_chain3c); the check of 1-3 must then fail (exit 1)."""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stopcheck1057 as sc  # noqa: E402

mutate = "--mutate" in sys.argv
chain = "ks_chain3c" if mutate else "ks_chain3b"
base = f"I966-dh370/{chain}/leg13_D260.8483_ks293/"
good = base + "anm_pin3_D261.0123.npz"
dup = base + "anm_pin3_D260.6706.npz"
noise = [f"I966-dh370/{chain}/leg12_D260.8483_ks293/jet_pin3_D260.8483.npz", f"I966-dh370/{chain}/leg12_D260.8483_ks293/pred_pin3_D261.0059.npz",
         base + "anm_run.log", base + "pred_pin3_D261.0123.npz"]
ok = True


def check(label, cond):
    global ok
    print(f"{'ok  ' if cond else 'FAIL'} {label}")
    ok &= bool(cond)


# 1: sync949.sh's pattern, from the script itself; the listing step keeps only paths under ks_chain3b/ (its ls-tree prefix)
src = open(os.path.join(HERE, "sync949.sh")).read()
pat = re.search(r"grep -E '([^']*)'", src).group(1)
listed = [p for p in [good, dup] + noise if "I966-dh370/ks_chain3b/" in p]
kept = subprocess.run(["grep", "-E", pat], input="\n".join(listed) + "\n", capture_output=True, text=True).stdout.split()
check("sync949.sh copies the leg 13 anm_pin3 states and nothing else", kept == [p for p in (good, dup) if p in listed])

# 2: queue_new949.py --dry on a temp HOME whose scratch949 holds what sync949.sh copies (the two anm_pin3 states)
with tempfile.TemporaryDirectory() as tmp:
    for p in (good, dup):
        os.makedirs(os.path.join(tmp, "scratch949", os.path.dirname(p)), exist_ok=True)
        open(os.path.join(tmp, "scratch949", p), "wb").close()
    out = subprocess.run([sys.executable, "-I", os.path.join(HERE, "queue_new949.py"), "--dry"], env=dict(os.environ, HOME=tmp), capture_output=True, text=True).stdout
queued = [l.split()[-1] for l in out.splitlines() if l.startswith("would queue")]
check(f"queue_new949.py --dry queues exactly c3b_ks293_D261.0123 (got {queued}); the already queued D260.6706 is skipped", queued == ["c3b_ks293_D261.0123"])

# 3: stopcheck1057.pushed_unread
unread, other = sc.pushed_unread([good, dup] + noise, {"c3b_ks293_D260.6706", "c3b_ks293_D260.8483"})
check(f"stopcheck1057.pushed_unread lists exactly c3b_ks293_D261.0123 (got {unread}), no state with another ks (got {other})", unread == ["c3b_ks293_D261.0123"] and other == [])

print("leg13_check1057: " + ("all ok" if ok else "FAILED"))
sys.exit(0 if ok else 1)
