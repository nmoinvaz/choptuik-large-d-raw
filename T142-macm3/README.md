# T142-macm3: the junk-frozen full-system step on a grid of chain_fit states

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0; its octo kernel checked bit for bit in T133), main 9330ffce (full_release.py
unchanged since 93a33a3, no rebuild). Comms entry: 2026-11-07 10:20 UTC cloud to macm3 (T142), after T139 stops.

T137's junk-frozen full-system step from T138's chain_fit states, so the held-harmonics bias of chain_fit is measured
about every 10 in D. From hp/ with venv-macm3, nice 10 under caffeinate -i, 6 threads, one state at a time:

  full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 6 --threads 6 > T142-macm3/release_D<D>.log

States in order: anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz (control), then T138-win2 chain/ or chain_o/
anm_pin3_D<D>.npz at D 130, 180, 110, 160, 205, 90, 120, 140, 170, 190, 209. Each has release_D<D>.cmd beside its log,
and exits.txt has how each ended. Control: the first line must read "residual at the pinned state 4.28e-18, Delta
1.7699262589377422" (as T141-win2/release_D79.7657.log), and the first step's dDelta +5.03e-8 within 2%. A state stops
after 6 steps or 1.5 h; T142 stops if swap use passes 2 GB.
