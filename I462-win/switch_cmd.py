"""#462: the launcher of a chain's restart with --held_o 1 --reseed_o 3 on main 7b6afc2 (the coordinator's rule: when a
step of a chain needs more than 6 octo-double solves, let it finish and save, stop that chain, restart it from its last
state with these two options and --base_polish 0).

    python3 switch_cmd.py CHAIN [--dry]        CHAIN is d6 or d10, run from the raw clone's I462-win folder

Writes CHAIN_long2.cmd: the chain's long-run command with the checkout choptuik-t151b (7b6afc2), --held_o 1 --reseed_o 3,
the newest saved state of the chain as --state, run_capped.py with the seconds left to that chain's cap (computed
here, not by hand), the log appended to chain_CHAIN.log and the exit code in chain_CHAIN_long2.exit. It refuses when
the newest state's D does not match the log's last accepted step (a step not saved yet), or when the cap is out of range.
--dry prints the command and writes nothing."""
import datetime as dt
import glob
import os
import re
import sys

CAPS = {"d6": dt.datetime(2026, 11, 11, 15, 31, 10, tzinfo=dt.timezone.utc),
        "d10": dt.datetime(2026, 11, 11, 15, 31, 6, tzinfo=dt.timezone.utc)}
chain = sys.argv[1]
dry = "--dry" in sys.argv
assert chain in CAPS, "CHAIN must be d6 or d10"
here = os.path.dirname(os.path.abspath(__file__))
states = glob.glob(os.path.join(here, f"chain_{chain}", "anm_pin3_D*.npz"))
dmax = {float(re.search(r"anm_pin3_D([0-9.]+)\.npz$", s).group(1)): s for s in states}
d_new = max(dmax)
state_rel = f"I462-win/chain_{chain}/{os.path.basename(dmax[d_new])}"
acc = [float(m.group(1)) for m in (re.search(r"^    a [0-9.]+ -> D ([0-9.]+):", ln) for ln in open(os.path.join(here, f"chain_{chain}.log"), encoding="utf-8", errors="replace")) if m]
d_log = acc[-1]
if abs(d_new - d_log) > 2e-4:
    sys.exit(f"REFUSED: newest state D {d_new} but the log's last accepted step is D {d_log} (not saved yet?)")
now = dt.datetime.now(dt.timezone.utc)
secs = int((CAPS[chain] - now).total_seconds())
if not 2 * 3600 < secs < 24 * 3600:
    sys.exit(f"REFUSED: {secs} s to the cap is out of range")
lines = [
    "@echo off",
    r"cd /d C:\Users\nathan\Source\choptuik-t151b\hp",
    r"set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%",
    r"set RAW=..\..\choptuik-large-d-raw",
    rf"python.exe -u %RAW%\I462-win\run_capped.py {secs} python.exe -u anm_run.py %RAW% %RAW%\I462-win\chain_{chain} --state {state_rel} --kfreeze 3 --held_fit data/held_fit_{chain}.json --N 24 --eps 1e-14 --h_max 1.0 --steps 400 --D_max 400 --threads 3 --corrector od --tol_od 1e-40 --qd_it 12 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1 --od_junk 0 --base_polish 0 --held_o 1 --reseed_o 3 >> %RAW%\I462-win\chain_{chain}.log 2>&1",
    rf"echo %errorlevel% > %RAW%\I462-win\chain_{chain}_long2.exit",
]
print(f"{chain}: state {state_rel} (D {d_new}, the log's last accepted D {d_log}); now {now:%Y-%m-%d %H:%M:%S} UTC, cap {CAPS[chain]:%Y-%m-%d %H:%M:%S} UTC, SECONDS {secs} ({secs / 3600:.2f} h)")
if dry:
    print("--dry, not written:\n" + "\n".join(lines))
else:
    open(os.path.join(here, f"{chain}_long2.cmd"), "w", newline="").write("\r\n".join(lines) + "\r\n")
    print(f"written {chain}_long2.cmd")
