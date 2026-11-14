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

## Delta_full - Delta_held at D 113, 117, 120

| D | #742 (stored full - stored held) | rounded, held polished (stored full - H_R) | exact (E - H_E) | exact - #742 | held: H_E - H_R (projector) | held: H_R - stored (its own convergence) |
|---|---|---|---|---|---|---|
| 113 | +4.365506e-13 | not run | not run | not run | not run | not run |
| 117 | +4.945575e-13 | not run | not run | not run | not run | not run |
| 120 | +5.322591e-13 | not run | not run | not run | not run | not run |
  #742's value at D 113 reproduced from the stored states: +4.3655e-13 (#742 +4.3655e-13) ok
  #742's value at D 117 reproduced from the stored states: +4.9456e-13 (#742 +4.9456e-13) ok
  #742's value at D 120 reproduced from the stored states: +5.3226e-13 (#742 +5.3226e-13) ok

all checks passed
