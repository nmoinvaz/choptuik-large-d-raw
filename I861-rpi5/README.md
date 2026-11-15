# I861-rpi5: Theorem A(M = 5)'s remaining lemmas (step (i) tables, lemma S and its scan, lemma 6a(5) at p̂) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/861. Script (the coordinator's): `run861.sh`, from `solver/proof/` of
the worktree `~/Source/choptuik-large-d-861` (wip/i861-rpi5 at origin/main 48a04e0d), one process at a time at nice 10,
every output written here and none into `lemmas_M_runs/`. Exits and wall times in `exits_861.txt`; versions in `env.txt`.

- `fpm_table5.log`, `fixed_point_M_table_M5.json`: step (i)'s table (`fixed_point_M.py --table --Ms=5`).
- `fpm_data5.log`, `fixed_point_M_data_M5.json`: step (i)'s data table (`--data-table`).
- `sector5.log`, `lemma6_sector_M5_rp0.08_1e-6.json`: lemma S, the old sector lemma and the flat estimate; `sector5_series.log`
  is its series control (`--mutate=series`, must fail).
- `scan5.log`, `lemmaS_scan_M5.json`: lemma S's scan.
- `jump5.log`, `lemma6a_M5_sub1e-18_phat.json`, `B_M5_sub1e-18_phat.json`: lemma 6a(5) at the certificate's p̂ (`centre_passed.txt`),
  with #184's commands; `jump5_partial`, `jump5_coords`, `jump5_swap` are its controls, `bfloat` and `bfloat_w` #39's float
  check of B and its control.
- `jump5_macB.log`, `lemma6a_M5_macB.json`: macm3's stored B (`I184-macm3`) loaded on the Pi.
