# I852-mac tables (tables.py)

max|z_h| 1.000111062; 3 steps

## The unperturbed path (C5)

| k | max\|u_k − u_(k−1)\| / max\|z_h\| | max\|F\| before | below 1e-90 | below 1e-93 | below 1e-96 |
| --- | --- | --- | --- | --- | --- |
| 1 | 3.2085e-57 | 1.7135e-66 | no | no | no |
| 2 | 2.3719e-98 | 2.3956e-79 | yes | yes | yes |
| 3 | 1.1622e-99 | 5.4062e-94 | yes | yes | yes |

max|F| at u_3: 4.5069e-94

## The perturbed paths (C4)

| run | e_0 | e_1 | e_2 | e_3 | gain e_1 / e_0 | reading |
| --- | --- | --- | --- | --- | --- | --- |
| m_h, a_h seed 1 rel 1e-90 | 1.0000e-90 | 1.0062e-86 | 1.7251e-99 | 2.7269e-99 | 1.0062e+04 | does NOT contract |
| m_h, a_h seed 1 rel 1e-93 | 1.0000e-93 | 9.3068e-90 | 2.0136e-99 | 1.7348e-99 | 9.3068e+03 | does NOT contract |
| m_h, a_h seed 1 rel 1e-96 | 1.0000e-96 | 9.3060e-93 | 1.2972e-99 | 1.8359e-99 | 9.3060e+03 | does NOT contract |

excess at rel 1e-90: (gain(1e-90) - gain(1e-96)) / 1e-90 = 7.5556e+92
e_k at k >= 2 over all rels: 1.2972e-99 .. 2.7269e-99; the unperturbed step at k = 3: 1.1622e-99

## The controls (C2, C3)

| run | e_0 | e_1 | e_2 | reading |
| --- | --- | --- | --- | --- |
| ctl_nostep_D240: m_h, a_h seed 1 | 1.0000e-96 | 1.0000e-96 | 1.0000e-96 | does NOT contract |
| ctl_centre_D240: centre seed 1 | 9.9987e-91 | 2.9742e-99 | 2.5172e-99 | contracts |
