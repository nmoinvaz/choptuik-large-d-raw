# I241-macm3: D 53.79, 54.04 and 55.04 recounted at M 48, kf 23 with one fixed left column (--aLL=-0.096 --aL=0.124)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon rebuilt on main 1bad14fd, modecount_cx for 3.14),
main 8c7c49d or later. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/241. Starts after #231's rebuild control passed (I231-macm3/control_D55_M32); runs beside I231's two M 40 counts (3 + 2 threads).

Inputs: the earlier caches, copied into D53/data (I237-macm3/D53), D54/data (I240-macm3) and D55/data (I232-macm3/D55): ONLY the evals files (modecount_<tag>_evals.jsonl), not the cp -R of the whole folder the issue lists, so that the
old logs and records do not mix with the new ones (a deviation in file selection, the caches are what the issue wants reused). The saved kf 23 states of those runs (hp_data_after/ of the same folders) are copied into hp/data before the
run so that setup loads them: the cached determinants and the new ones then come from the same state, which re-converging could change in the last bits (the rebuild control covers M 32 only). They are moved out again afterwards.
The state files' sha256 are in states_sha256.txt.

Commands (D53/count.cmd, D54/count.cmd, D55/count.cmd, caffeinate -is, nice 10, one thread each, from the repository root): python3 hp/modecount_wind.py hp/data/states/up10_D53.7914.npz --M=48 --kf=23 --h0=0.6
--lam=2.048648769709809 --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=D53.7914_M48_kf23 --data=<raw>/I241-macm3/D53/data; D54: up10_D54.0414.npz --lam=2.048451702933493; D55: up10_D55.0351.npz --lam=2.04768412771239.

Written before the run. The fixed edges are stated in every table (Re -0.096 and 0.124 as the left column; the other edges are the automatic ones, which move with D: a1, a2, aR are not fixed). Table: the 8 boxes at each D with both
mismatch counts per edge (all passes and the last pass), and the number of new determinants per D (the cache reuse is verified by the line count before and after: lines already present must be unchanged, cmp of the first lines).
Reading rules, fixed now: (1) B0 and U0 are the same region at the three D (Re -0.096 to 0.124). The onset in (53.79, 54.04] is "confirmed" when B0 and U0 are 0 at D 53.79 and nonzero at D 54.04 and D 55.04, "not confirmed" otherwise
(then reported as it is, with the windings). (2) A zero crosses from U0 to U between D 54.04 and 55.04 when U0 drops and U rises by the same amount with the fixed edge (U is the strip right of Re 0.124, with its own automatic right edges);
if U0 and U do not change like that, the difference at the automatic edges was the box edge. (3) An edge that passes too close to a pole and does not resolve is reported as "not a count"; the edge is not moved. No zero is located.
