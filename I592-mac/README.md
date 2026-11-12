# I592-mac: the complex zeros of x - c from the horizon series at D 40, 73 and 242.36, against the series radius

Machine: the M5 Mac (coordinator). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/592

Code: choptuik-large-d `hp/pole_sonic.py` at 5c10e6f, run from `hp/` with the python of `/Users/nathan/venv-314`:

    python3 -u pole_sonic.py pole_sonic.jsonl data/states/up7_D40.0201.npz RAW/T75/pin7_D73.2657.npz \
      RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2

The states are those of I545-mac (same sha256). Pade orders 24 and 32, all 32 lanes, delta = +-1e-8, +-1e-6, +-1e-4.

- `pole_sonic.log`: the planted check (pass), then one line per (state, delta).
- `pole_sonic.jsonl`: per (state, delta) the nearest zero (u, |u|, arg, lane, the two orders' agreement), |u| / R, the verdict, and every lane's nearest zero with 1 - c_0 (0 at every lane).
