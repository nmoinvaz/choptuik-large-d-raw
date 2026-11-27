# I1098-dh610/ladder/D4628_x706: D 4628's M 32 stages with the last node at 0.7062221 (#1098)

Machine: dh610 (Fedora, i7-12700), fastmul7 (hp_z, site_z at c21ba40d), 8 threads. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

`d4628d_610.sh` (unit i1088a-d4628d): the guess (`guess/`, form_s_lastnode.py guess, deg 2 in 1/n from #1088's lastnode
states at D 4000, 5657 and 8000 carried to x_l 0.7062221, D 8000's L = 20 node, L 11.6 here; why: `../D4628_guess`),
then form_s.py jump from it (deg 0, held, a 11.565, ks 6959, kc 260, it_max 12) into `jump/`; `pre.log` logs both.
When the jump converges, the unit stops i1088a-d4628b (the jump at x_l 0.7035589, L 46), i1088a-d4628c and
i1088a-ksdown3 (both waiting on it), installs the downward ks gate (3b3bfc60) and ladder_point2.sh blob e0cf5880, and
runs the point from the kept jump: KSGATE_EXTRA="--down 1 --step 100", KSBAR 1e-64, STOP_AFTER=rls13, chord-free,
kc 260 (`run.log`, `rls/`, `rls13/`).
