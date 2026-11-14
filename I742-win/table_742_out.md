reading check: Delta_full - Delta_held at D 113 from I739-win/B = +4.3655e-13 (#739: +4.3655e-13) ok
control (a): the D 113 start re-polished (P/base_pin13_D113.0000.npz), Delta - B's Delta = +0.0000e+00; Delta 1.733640141567942734406710993193602081591; bar 1e-30: met

### per attempt

| run | step | from D | a | to D | corrector steps | seconds | max abs F at the end | converged (at most 1e-60) | accepted |
|---|---|---|---|---|---|---|---|---|---|
| P | 0 | 113 | 1 | 114 | 5 | 548 | 8.50e-69 | yes | True |
| L | 0 | 114 | 1 | 115 | 5 | 615 | 1.70e-68 | yes | True |
| L | 1 | 115 | 1 | 116 | 5 | 645 | 2.30e-62 | yes | True |
| L | 2 | 116 | 1 | 117 | 5 | 603 | 1.80e-64 | yes | True |
| M | 0 | 117 | 0.5 | 117.5 | 6 | 897 | 8.60e-79 | yes | True |
| M | 1 | 117.5 | 0.5 | 118 | 6 | 918 | 6.90e-74 | yes | True |

### Delta_full - Delta_held

| D | Delta_full (octo-double, 40 digits) | Delta_full - Delta_held | delta_all.csv err (kind) | ratio to the err | ratio of the shift to the previous D's |
|---|---|---|---|---|---|
| 113 | 1.733640141567942734406710993193602081591 | +4.3655e-13 | 3.0e-12 (chain_fit) | 0.146 |  |
| 114 | 1.732869663158360015225732667964316431814 | +4.5175e-13 | 3.2e-12 (chain_fit) | 0.141 | 1.0348 |
| 115 | 1.732112314608397196279780335037996998181 | +4.6652e-13 | 3.3e-12 (chain_fit) | 0.141 | 1.0327 |
| 116 | 1.731367762815444921564320564141065073226 | +4.8080e-13 | 3.5e-12 (chain_fit) | 0.137 | 1.0306 |
| 117 | 1.730635685860038849267059677903292989227 | +4.9456e-13 | 3.7e-12 (chain_fit) | 0.134 | 1.0286 |
| 118 | 1.729915772540067188606164966063807771721 | +5.0775e-13 | 3.8e-12 (chain_fit) | 0.134 | 1.0267 |
| 119 | not reached | | | | |
| 120 | not reached | | | | |
