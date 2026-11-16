# I875-mac tables (tables.py)

I874-mac/anm_pin3_D240.1244_u2.npz: max|z_h| 1.000111062; 2 steps

## The unperturbed path (C4)

| k | max\|u_k − u_(k−1)\| / max\|z_h\| | max\|F\| before | below 1e-90 | below 1e-93 | below 1e-96 |
| --- | --- | --- | --- | --- | --- |
| 1 | 1.5634e-99 | 5.4062e-94 | yes | yes | yes |
| 2 | 2.8286e-99 | 4.5783e-94 | yes | yes | yes |

max|F| at u_2: 6.6719e-94

## The perturbed paths (C3)

| run | e_0 | e_1 | e_2 | gain e_1 / e_0 | e_1 / e_0² | reading |
| --- | --- | --- | --- | --- | --- | --- |
| m_h, a_h seed 1 rel 1e-90 | 1.0000e-90 | 7.5556e-88 | 3.0684e-99 | 7.5556e+02 | 7.5556e+92 | does NOT contract |
| m_h, a_h seed 1 rel 1e-93 | 1.0000e-93 | 7.5556e-94 | 8.8728e-100 | 7.5556e-01 | 7.5556e+92 | contracts |
| m_h, a_h seed 1 rel 1e-96 | 1.0000e-96 | 1.9861e-99 | 1.3679e-99 | 1.9861e-03 | 1.9861e+93 | contracts |

## The gain from the two starts

#852: I603-win2/chain/anm_pin3_D240.1244.npz; #875: I874-mac/anm_pin3_D240.1244_u2.npz

| rel | gain, #852 (stored truth) | gain, #875 (u2) | #852 less #875 | #852 / #875 |
| --- | --- | --- | --- | --- |
| 1e-90 | 1.0062e+04 | 7.5556e+02 | +9.3060e+03 | 1.3317e+01 |
| 1e-93 | 9.3068e+03 | 7.5556e-01 | +9.3060e+03 | 1.2318e+04 |
| 1e-96 | 9.3060e+03 | 1.9861e-03 | +9.3060e+03 | 4.6855e+06 |
