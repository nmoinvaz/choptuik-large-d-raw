# I580-dh370: near_null_eq.py's layout ladders at crawlJ's D 242.3642 on main's exact projector (dh370, Fedora Linux 45)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/580
Code: choptuik-large-d main at e835d9469626943b184d830cee00ffbd257dd4d8 (the code of 083ac99 and the exact projector of
1658a4f are in it), worktree `choptuik-large-d-604` with the kernel built in I604-dh370/.
Runs: `python near_null_eq.py RAW STATE --plant=7 --cr_floor=F --threads=4 --json=OUT` from `hp/`, at the four layouts
(0.70: `I461-win2/crawlJ/anm_pin3_D242.3642.npz`; 0.80: `I543-win2/renode_last080_D242.3642.npz`; 0.92:
`I554-win2/renode_last092_D242.3642.npz`; 0.975: `I562-win2/renode_0975_D242.3642.npz`) and F = 1e-12, 1e-14, 1e-10.
Criteria: as fixed in the issue's comment of 2026-11-12 09:06 UTC.

## Files

| file | what |
|---|---|
| eq_LAY_FF.json, eq_LAY_FF.log | one `near_null_eq.py` run, layout LAY (070, 080, 092, 0975) and floor FF (1e-14, 1e-12, 1e-10, or 0 for the control), the log ends with `wall`, `maxrss` and `exit` |
| ladders580.sh | the 12 runs at F > 0, three at a time (exits: 0 at 0.92 and 0.975 for F = 1e-12 and 1e-14, 1 for the other eight, which failed the planted check) |
| f0_580.sh | the four control runs at F = 0 on the same kernel (all exit 0, planted check passes) |
| ladder_table.py, ladder_table.txt | the tables of the issue's summary, from the json files and the F = 0 files of I505-win2, I543-win2 and I554-win2 |

A first start of the F = 0 runs was killed by a reboot of the machine and run again; the partial logs were overwritten.
