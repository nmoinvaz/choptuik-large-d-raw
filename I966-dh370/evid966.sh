#!/usr/bin/env bash
# #966: copies the in-flight attempt's corrector log lines into the raw folder (coordinator's hc 2026-11-19 09:3x UTC):
# eval340_<leg>_a<a>.txt = the attempt's section of anm_run.log (from its a_rule line to the end), and the trial / chord
# lines whose evaluation took 300 s or more, with a count and the time sums. usage: bash evid966.sh [tag]
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1); LOG=${LEG}anm_run.log
python3 -I - "$LOG" "$OUT" "${1:-}" <<'PY'
import re, sys
log, out, tag = sys.argv[1:4]
L = open(log, errors="replace").read().splitlines()
st = max(i for i, l in enumerate(L) if re.match(r"\s+a_rule reseed:", l))
sec = L[st:]
a = re.search(r": a ([0-9.]+)\s*$", sec[0]).group(1)
leg = log.split("/")[-2]
tr = [l for l in sec if re.search(r"trial lam [0-9.]+: .*, [0-9.]+ s$", l)]
big = [l for l in tr if float(re.search(r", ([0-9.]+) s$", l).group(1)) >= 300]
ch = [l for l in sec if re.match(r"\s+on \d+: strong chord", l)]
name = f"{out}/eval340_{leg}_a{a}{tag}.txt"
with open(name, "w") as f:
    f.write(f"# {leg} attempt a {a} (anm_run.log lines {st + 1}..{len(L)} at copy time)\n")
    f.write(f"# trials {len(tr)}, of 300 s or more {len(big)}, seconds of those {sum(float(re.search(r', ([0-9.]+) s$', l).group(1)) for l in big):.0f}\n")
    f.write("# the trial lines of 300 s or more, then the whole attempt section\n")
    f.write("\n".join(big + ch) + "\n\n# ---- attempt section ----\n" + "\n".join(sec) + "\n")
print(name, len(tr), len(big))
PY
