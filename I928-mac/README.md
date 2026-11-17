# I928-mac: the sigma-model kernel's chain in D past D 11 at eta 0.3 and 1, with its growth rates

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/928. Code: branch `wip/sa-928`
on main f9833796 (`matter/sigma_ms`: `chain.py`, `run_eta.py --solver band`, `mode_lam.py`, `mode_table.py`). The
kernel is #918's build with the mode matrix (`I918-mac/README.md`), run with python 3.14, one process with 2 threads
at nice 10, without a load gate (the issue's terms). The load at each start is in `out/runs.log` and in the `start`
lines of `out/lam_*.txt`. Local paths are removed from the copies here.

This file is the pilot's state. It is rewritten when the runs end.

## The pilot (`run_pilot.sh`, `seg.sh`; `out/chain_eta*_D11_11.125.txt`, `out/lam_eta*_D11_11.125.txt`)

Two points past D 11 at each coupling, from #916's and #917's states at D 10.9375 and 11 (`seeds/`), then their
rates. The load was 62 to 134.

| eta | D | Delta | max \|F\| | band solver's steps | lambda_g | gauge root within | lambda | gamma = 1/lambda |
|---|---|---|---|---|---|---|---|---|
| 0.3 | 11.0625 | 1.133738940731172 | 6.0e-29 | nrrbbb, 16 min | 0.811337996698 | 1e-12 | 2.962535926279 | 0.337548649159 |
| 0.3 | 11.125 | 1.132699643104875 | 4.1e-29 | nrrbbb, 16 min | 0.811512331759 | 1e-12 | 2.957645049277 | 0.338106832747 |
| 1 | 11.0625 | 1.015116072303529 | 7.7e-30 | nnnrrbbbn, 22 min | 0.822594391567 | 1e-12 | 2.858913434134 | 0.349783238646 |
| 1 | 11.125 | 1.014542836444146 | 2.4e-30 | nnnrrbbbn, 22 min | 0.822641959143 | 1e-12 | 2.854570140766 | 0.350315441796 |

The gauge root is enclosed by two determinants, at lambda_g - 1e-12 and lambda_g + 1e-12, whose signs differ
(`mode_lam.py --gauge_window 1e-12`). A rate takes 10 determinants, 57 to 67 s each at this load.

First differences of lambda per unit D, from D 11 (#918: 2.967495609 at eta 0.3, 2.863317652 at eta 1): -0.07935
and -0.07825 at eta 0.3, -0.07047 and -0.06949 at eta 1. The step before D 11 was -0.0822 and -0.0730 per unit D.
