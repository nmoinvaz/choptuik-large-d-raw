# I545-mac: the perturbed horizon solution marched past the series radius at D 40, 73 and 242.36

Machine: the M5 Mac (coordinator). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/545

Code: choptuik-large-d `hp/pole_march.py` at d94c86d. Run from `hp/` with the python of `/Users/nathan/venv-314`
(Python 3.14, hpkernel of main):

    python3 -u pole_march.py pole_march.jsonl data/states/up7_D40.0201.npz RAW/T75/pin7_D73.2657.npz \
      RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --deltas=1e-8,1e-6,1e-4,-1e-8,-1e-6,-1e-4

States (sha256, first 16 hex): up7_D40.0201 dc5f2053880e5494, T75/pin7_D73.2657 efa91079132b87b3,
I461-win2/crawlJ/anm_pin3_D242.3642 557f4078a0206bfe (read as its top two parts).

- `pole_march.log`: the planted check (pass), then per state the control and one line per delta.
- `pole_march.jsonl`: one record per (state, delta): R (13.6's estimator), the start R/2, the breakdown, the shadow's
  trusted range, the closest approach to x = c (`near_sonic`), the zeros of x - c and B, and the march subsampled to
  about 60 points (u, max x - c, min B, max |field|, step).

Exit 1: the series control fails at D 73.27 (4.6e-3 against a shadow of 3.9e-17) and D 242.36 (4.5e2 against
1.6e-13). It passes at D 40.02 (1.0e-23 against 4.2e-24).
