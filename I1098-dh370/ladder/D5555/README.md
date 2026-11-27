# I1098-dh370/ladder/D5555: D 5555's M 32 stages by recipe v2's amendment 2, on fastmul6 (#1098)

Machine: dh370 (Fedora 45, i7-8700, 12 threads, 31 GB), 6 threads. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 01:36 UTC): D 5555 moves here from dh610's chain (dh610 is busy for about 10 h).

`d5555_370.sh` (unit i1088a-d5555b) runs `ladder_new.sh` (raw c281b00d3, I1098-mac-a/tools, blob 3039e5b9), with these settings:
- **Kernel:** fastmul6's Skylake wheel (site_sky, d368a0c0), not fastmul7. The coordinator accepted it for this point because D 1291's kernel cross-check moved Delta by 0.0 to 60 digits. That check released h23 and h25 again on fastmul7 from the fastmul6 h21 state. The Moebius values carry fastmul6's 1.7e-60 split offset, which fastmul7 removes.
- **Python:** `hp_y5555`, a copy of hp_y (f398e829). Its ks_gate.py is wip/large-d-form-s 3b3bfc60's (blob a91c7363), installed in the copy only.
- **Layout:** x_l 0.7062221, D 8000's L = 20 node, so L = 13.9 here.
- **Guess:** form_s_lastnode.py guess, deg 2 in 1/n, from #1088's lastnode states at D 4000, 5657 and 8000 (in `../inputs`, checked by blob). dh610's ratio test read 7.5e-13 for it (I1098-dh610/ladder/D4628_guess/ratio_hi.log).
- **Jump:** deg 0 from the guess: held, a 13.8825, ks 8350, kc 260. Then ladder_point2.sh (e0cf5880) with the downward ks gate from ks0 6660, KSBAR 1e-64, chord-free, through rls13.
- **Logs:** `setup.log`, `pre.log` (guess and jump), then ladder_point2.sh's `run.log`, `jump/`, `rls/` and `rls13/`.
