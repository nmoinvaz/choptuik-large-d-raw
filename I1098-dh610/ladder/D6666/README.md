# I1098-dh610/ladder/D6666: D 6666's M 32 stages by recipe v2's amendment 2 (#1098)

Machine: dh610 (Fedora, i7-12700), fastmul7 (hp_z, site_z at c21ba40d), 10 threads. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 02:35 UTC): D 6666 moves here from mm5's queue, into dh610's idle threads beside D 4628.

`d6666_610.sh` (raw 1d67f29d4 I1098-mac-a/tools, blob 1bb8ec38; unit i1088a-d6666, TC c281b00d3, THREADS 10) runs `ladder_new.sh`:
- **Layout:** x_l 0.7062221 (D 8000's L = 20 node), so L = 16.7 here.
- **Guess:** deg 2 in 1/n from #1088's lastnode states at D 4000, 5657 and 8000 (`../D4628_guess/inputs`, checked by blob). dh610's ratio test read 3.7e-12 for it.
- **Jump:** deg 0 from the guess: held, a 16.66, ks 10016, kc 260.
- **Then:** ladder_point2.sh (e0cf5880) with the downward ks gate from ks0 8000 (KSBAR 1e-64), chord-free, through rls13.
- **Logs:** `setup.log`, `pre.log` (guess and jump), then ladder_point2.sh's `run.log`, `jump/`, `rls/` and `rls13/`.
