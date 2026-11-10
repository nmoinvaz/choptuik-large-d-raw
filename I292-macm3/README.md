# I292-macm3: the two lam_phys circles of #282 at R 0.0125 and 0.003 (D 55.04, M 64, kf 23, with the centre node (node/) and without (nonode/))

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/292. Beside I251, I273, I285, I290 and I291.

Commands (run.sh, caffeinate -is, nice 10, one thread, (a) then (b)): the coordinator's comment as written. The saved states of #275 and #252 are copied into
hp/data first (state_sha256.txt, equal to I282's), so each setup should load without a refit; a Newton or LM line is reported. Both caches start empty.

Written before the run (coordinator's reading rule, copied). A miss that falls in proportion to R on both layouts is the circle's own zero estimate, whose error scales
with R times the determinant's relative noise. A miss that stops falling is a floor, reported with the R where it sets in. Stop, per layout: a setup missing the
1e-15 gate, (a) without a node at 0.15, or (b) with one. A circle that does not wind +1 is reported and the run continues. The reference is lam(64, kf 23) = 2.047684127603771
(I291-macm3), 1.1e-10 from the centre 2.04768412771239. Estimates are the circles' own ranges, not bounds.

## Results

