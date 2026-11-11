# I466-macm3: the lambda_phys circle at R 0.05 and 0.0125 on the D 61.03 M 48 kf 27 and kf 25 states (does the miss fall with R, as at M 64?)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/466.
Raw output is not committed here while the raw repository's rewrite pause lasts.

States: I280-macm3/hp_data_after/modecount_state_D61.0264_M48_kf27.npz and I244-macm3/kf25/hp_data_after/modecount_state_D61.0264_M48_kf25.npz, copied into hp/data so the setups load them with no refit (sha256 in state_sha256.txt).
Command (run.sh, caffeinate -is, nice 10, one thread, kf 27 then kf 25): hp/modecount_circle.py on hp/data/seeds/local/up23_D61.0264.npz with the centre 2.043532530673195 (the M 32 lambda_phys; the roots of #460 are 5.7e-12 and 3.2e-11 from it),
radii 0.05 and 0.0125, --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kfK --data=<raw>/I466-macm3/kfK/data. The caches start empty (the R 0.2 circles of #244 and #280 use other points).

Written before the run (the issue's). Miss and estimate against R at both cuts, measured from #460's roots (kf 27: 2.0435325306789354, kf 25: 2.043532530641384), beside the R 0.2 rows (kf 25: 2.043535 +0.000004i, 4.7e-6 from its root, estimate 9.5e-7; kf 27:
2.043502736 -0.000013053i, 3.25e-5, estimate 1.3e-5). A floor is reported if the miss stops falling with R (a miss that falls in proportion to R is the circle's own zero estimate, as #292 read it). Estimates are ranges, not bounds.

## Results

Both cuts exit 0 (kf 27 18:01:53 to 18:56:12 UTC, kf 25 to 19:36:32 UTC; 60 determinants each, caches started empty). Both states loaded with no refit (|F| 1.3e-19). Every circle winds +1 with 28 points, 0 mismatches, 0 alias bisections. Miss is from #460's roots (kf 27 2.0435325306789354, kf 25 2.043532530641384):
  kf 27: R 0.05 zero 2.0435360258 +0.0000049392i miss 6.05e-06 (estimate 5.6e-06); R 0.0125 zero 2.0435324953 -0.0000008548i miss 8.6e-07 (2.3e-06).   kf 25: R 0.05 zero 2.0435337790 -0.0000003324i miss 1.29e-06 (2.2e-07); R 0.0125 zero 2.0435321277 -0.0000000803i miss 4.1e-07 (7.1e-08).
