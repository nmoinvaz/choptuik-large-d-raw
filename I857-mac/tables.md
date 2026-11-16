# I857-mac tables (tables.py)

## The starts

| start | state | unperturbed dΔ | max\|d0\| / max\|z_h\| |
| --- | --- | --- | --- |
| truth | I603-win2/chain/anm_pin3_D240.1244.npz | -4.3765436014e-58 | 3.2085e-57 |
| u2 | I874-mac/anm_pin3_D240.1244_u2.npz | 5.7442945324e-103 | 1.5634e-99 |

## Seed 1 at each rel

| start | rel | move | dev | \|dev\| / move |
| --- | --- | --- | --- | --- |
| truth | 1e-83 | 1.686626e-83 | +1.838055e-83 | 1.089782 |
| truth | 1e-84 | 1.686626e-84 | +1.828131e-84 | 1.083898 |
| truth | 1e-85 | 1.686626e-85 | +1.827138e-85 | 1.083310 |
| u2 | 1e-83 | 1.686626e-83 | +1.697652e-83 | 1.006538 |
| u2 | 1e-84 | 1.686626e-84 | +1.687728e-84 | 1.000654 |
| u2 | 1e-85 | 1.686626e-85 | +1.686736e-85 | 1.000065 |

## Odd and even parts at the smallest rel (seeds 1 and 3)

| start | rel | p | dev(1) | dev(3) | odd L | L − 1 | even n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| truth | 1e-85 | 1.0024, 1.0002 | +1.8271382934e-85 | -1.8269177593e-85 | 1.0832444729 | +8.3244e-02 | 6.537732e-05 |
| u2 | 1e-85 | 1.0025, 1.0003 | +1.6867360215e-85 | -1.6865154874e-85 | 1.0000000000 | +0.0000e+00 | 6.537732e-05 |

## The cross term (C5): truth less u2

| rel | \|dev\| / move, truth | u2 | difference |
| --- | --- | --- | --- |
| 1e-83 | 1.089782 | 1.006538 | +8.324447e-02 |
| 1e-84 | 1.083898 | 1.000654 | +8.324447e-02 |
| 1e-85 | 1.083310 | 1.000065 | +8.324447e-02 |

difference over the rels: +8.324447e-02 .. +8.324447e-02, spread over rels 0.000e+00
odd part L at 1e-85: truth 1.0832444729, u2 1.0000000000, difference +8.324447e-02
even part n at 1e-85: truth 6.537732e-05, u2 6.537732e-05, difference +8.472e-17
per unit step: L's difference / (truth's max|d0| / max|z_h| 3.2085e-57) = 2.5945e+55
#850's quadratic: q = dev / rel^2 at rel 1e-67 1.102671e+81; its n at 1e-85, q rel^2 / move, 6.537732e-05; u2's n less it +4.200e-16 (+6.42e-12 of it)
#850's cubic at rel 1e-67 from its last p 1.9999999999728368: c rel -6.9495e-12; u2's n less q / (1 + c rel)'s n, as a part of it: -5.25e-13; the rounding of n from the stored doubles dev(1), dev(3) is at most 1.7e-12 of it (a bound)
