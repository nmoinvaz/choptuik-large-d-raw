# I228-win2: #82's K 45, J 1500 node at omega/omega_inf 1.10 rerun on win2's new firmware

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/228 (recommended by win2 in #202's summary).

Command of #82 (`../I82-win2/run_i82_one.cmd`), from `solver/inner_amp/` of `D:\choptuik-large-d` (main checkout at 188853c,
`amp_flint_par.py` unchanged in code since #82's 700da3a, only docstring lines were added later), Normal priority, no affinity,
one thread per process:
`amp_flint_par.py 1.10 45 1500 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out <this folder>/sigF_w1.10_K45_J1500_p1280.json`
with the interpreter of #82, `venv-t126` (Python 3.12.8, python-flint 0.9.0 / FLINT 3.6.0, mpmath 1.3.0, numpy 2.5.4), so that
what changed against #82's run is the firmware (BIOS 3.40, microcode 0x122, ME 19.0.11.2289) and not the software (`run_i228.sh`,
`w1.10.log`, `exits.txt`). It starts when #213 has ended (its memory), the coordinator's order.

`compare_228.py` compares the new file with `../I82-win2/sigF_w1.10_K45_J1500_p1280.json` bit for bit (timing keys dropped,
`procs` kept, both 3), names the first differing entry and the first differing sigma string, and gives the difference of the
new file from win2's K 33 J 1000 value at 1.10 against #82's same-machine 1.09 and 1.11 rows (`--selftest`: a planted digit in
one sigma string is found at its index, a copy is equal).

## Result (2026-11-10 06:36 UTC)

Run: started 2026-11-09 15:30:00 UTC, exit 0 at 2026-11-10 06:20:46 UTC, wall 53 446 s (14 h 50 min), against 56 711 s for #82's node
(ratio 0.942). `compare_228.py` (`--selftest` ok), output in `compare_228_result.txt`:

- Part 1, bit for bit: **equal** (timing keys dropped, `procs` kept, both 3). Exit 0.
- Part 0, log against #82's `w1.10.log`: **identical through order 45** (276 lines, elapsed times removed).
- Part 2, distance from win2's K 33 J 1000 value at 1.10 (`../I202-win2`): the new row equals the old row (the files are equal),
  and is above the larger of the 1.09 and 1.11 same-machine rows at n = 6, 7, 15 and 16. The second acceptance bullet is not met,
  exactly as for #82's file, so it is a property of the node and not of the firmware.
- The sigma are unchanged, so `second_zero_nodes.py --k45` and #203's `second_zero.py real` were not rerun.

Machine over the run (`../I204-win2/sensor_log.txt`, 177 five-minute readings 15:34 to 06:19 UTC): utilization mean 77.2% (Windows
processor-utility counter, 8 to 135), package power mean 120.2 W (22.0 to 195.8), hottest core up to 104 C (17 readings at 104, TjMax
105), free memory 24.8 to 74.1 GB. One alert-only memory alert, 20.9 GB free at 2026-11-09 20:43:09 UTC (`../I256-win2/MEM_ALERT_2026-11-09_2043`),
nothing was killed or paused. No crash, WHEA, Kernel-Power 41, BugCheck or Application Error (1000, 1002) event since the watchers'
restart at 23:44 UTC on 2026-11-08 (event logs queried at 2026-11-10 06:36 UTC, `crash_watch.py` up, no ALERT file).
