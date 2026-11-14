# I785-dh610: v_1's share of the first step at the 0.975, 0.80 and 0.92 layouts in one build

Machine dh610 (Fedora 45, i7-12700; 4 threads beside #608's chains), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/785.

Scripts (written by the coordinator): `run785.sh` (I772-dh610's `uf688.py`, hp/ from HP688 = dh610's main checkout at
a879ccc3, at #688's start `I654-dh370/start/start_0975.npz`, taken from origin/main), and `share785.py` (its selftest
reads #688's line as 0.9356, the 94% of #688).

Criteria, fixed before the run (#785): uf688's controls a and b ok at 0.975; sigma_1 and u_1^T r against #688's
`uf_horizon.log` to 1e-5 relative (another build; the logs print 6 digits, one unit of which is up to 2e-6 relative,
so the issue's 1e-6 is read at the printed precision); v_1's share (v_1^T dz)^2 / |dz|^2 at 0.975 from this run and at
0.80 and 0.92 from #772's logs, one formula over the printed values. On the stored logs it gives 0.9356 (#688, 0.975),
0.4269 (0.80) and 0.6122 (0.92).
