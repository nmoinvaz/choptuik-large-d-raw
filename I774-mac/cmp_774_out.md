## Reading check

  reading I739-win/B/anm_pin13_D113.0000.npz: 1.733640141567942734406710993193602081591 = #742
  reading I742-win/L/anm_pin13_D117.0000.npz: 1.730635685860038849267059677903292989227 = #742
  reading I742-win/M/anm_pin13_D120.0000.npz: 1.728511242950407984923956924965683176416 = #742
  reading I727-win/X2c/base_pin13_D99.8750.npz (57 decimals): 1.745150028164499252944352893640343550633457431631616393443 = #727
  reading T138-win2/chain/anm_pin3_D113.0000.npz (12 decimals): 1.733640141568 = chain.log
  reading T138-win2/chain/anm_pin3_D117.0000.npz (12 decimals): 1.730635685860 = chain.log
  reading T138-win2/chain/anm_pin3_D120.0000.npz (12 decimals): 1.728511242950 = chain.log
  cross-check with #739's arb reading on 7 states: largest difference 0.0e+00 ok

## Control: C_X2c (build R, #727's X2c job from its start) against X2c's stored root

  Delta(C_X2c) - Delta(X2c stored) = +0.0000e+00; bar 1e-50: met
  all eight parts bit for bit equal to the stored X2c: True
  Newton lines against #727's X2c.log: 4 lines, all equal

## E_117 against #752's run on the same build (I752-mac/logs/AB_main.log, its base polish)

  5 lines against 5: all equal

## Shifts on the exact projector (build E) from the stored states

| state | D | start max\|F\| on E | Newton steps | final max\|F\| | converged (at most 1e-60) | Delta on E (40 digits) | stored Delta (40 digits) | shift = E - stored | kind | bar | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E_113 | 113 | 2.05e-34 | 4 | 9.13e-112 | yes | 1.733640141567942734310709655625123636920 | 1.733640141567942734406710993193602081591 | -9.6001e-20 | measured: exact - rounded, both converged roots on their own plan (stored on win's pre-#523 build) | 4.37e-16 | below the bar |
| E_117 | 117 | 2.01e-34 | 4 | 1.46e-106 | yes | 1.730635685860038849282734477817859081897 | 1.730635685860038849267059677903292989227 | +1.5675e-20 | measured: exact - rounded, both converged roots on their own plan (stored on win's pre-#523 build) | 4.95e-16 | below the bar |
| E_120 | 120 | 1.98e-34 | 4 | 1.58e-102 | yes | 1.728511242950407985000366909760210225118 | 1.728511242950407984923956924965683176416 | +7.6410e-20 | measured: exact - rounded, both converged roots on their own plan (stored on win's pre-#523 build) | 5.32e-16 | below the bar |
| E_cont3 | 99.875 | 2.20e-34 | 3 | 4.45e-69 | yes | 1.745150028164499252959346891093763008937 | 1.745150028164499252944352893640343550633 | +1.4994e-20 | exact - stored quad-double state; its od polish on the rounded build takes no Newton step (#727 pilot2) | 1.00e-25 | FLAG (above the bar) |
| E_X2c | 99.875 | 2.20e-34 | 3 | 4.45e-69 | yes | 1.745150028164499252959346891093763008937 | 1.745150028164499252944352893640343550633 | +1.4994e-20 | measured: exact - rounded, both converged roots on their own plan (stored on win's pre-#523 build) | 1.00e-25 | FLAG (above the bar) |

E_cont3 - E_X2c (one plan, both on E): +7.6439e-98; stored cont3 - stored X2c: -1.1101e-46

## Plan dependence at D 99.875: X2 on its own plan against X2c (cont3's plan)

  reading: stored X2 - stored X2c = -1.6580e-25 (#727: -1.6580e-25) ok
  R_X2: 1 Newton steps, start max|F| 8.59e-55, final 1.11e-77, converged True; Delta 1.745150028164499252944352727836252300100; minus stored X2 +5.5589e-45
  E_X2: 3 Newton steps, start max|F| 2.20e-34, final 4.45e-69, converged True; Delta 1.745150028164499252959346725289547222578; minus stored X2 +1.4994e-20
  plan dependence X2 - X2c: rounded -1.658041e-25, exact -1.658042e-25, exact - rounded -1.245e-31
  projector shift of X2 on its own plan (E_X2 - R_X2) +1.4994e-20 against X2c's +1.4994e-20

## Delta_full - Delta_held at D 113, 117, 120

| D | #742 (stored full - stored held) | rounded, held polished (stored full - H_R) | exact (E - H_E) | exact - #742 | held: H_E - H_R (projector) | held: H_R - stored (its own convergence) |
|---|---|---|---|---|---|---|
| 113 | +4.365506e-13 | +4.365506e-13 | +4.365505e-13 | -9.600e-20 | -3.6248e-27 | -1.0744e-31 |
| 117 | +4.945575e-13 | +4.945575e-13 | +4.945575e-13 | +1.567e-20 | -5.8163e-27 | -3.3265e-32 |
| 120 | +5.322591e-13 | +5.322591e-13 | +5.322592e-13 | +7.641e-20 | -2.4780e-27 | -2.9202e-34 |
  #742's value at D 113 reproduced from the stored states: +4.3655e-13 (#742 +4.3655e-13) ok
  #742's value at D 117 reproduced from the stored states: +4.9456e-13 (#742 +4.9456e-13) ok
  #742's value at D 120 reproduced from the stored states: +5.3226e-13 (#742 +5.3226e-13) ok

all checks passed
