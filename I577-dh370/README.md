# I577-dh370: setup and bit checks of the hp build on dh370 (Fedora Linux 45, i7-8700)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.

Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/577

## Contents

| file | what |
|---|---|
| selftest.log | `check_numbers.py --selftest` before hpkernel is built: exit 1, `ModuleNotFoundError: No module named 'hpkernel'` raised by the `hopf_law` check (check_numbers.py:208 imports hp/hopf_amp_mode.py, which imports hp/gamma_dd.py, which imports hpkernel) |
