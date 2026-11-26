# I1098-dh610/reconv622: D 622's kfree-15 system re-converged from its h15 state (#1098)

Machine: dh610 (Fedora, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

D 622's tail released h15 at the kfree-15 system's |F| 3.41e-51, so the gain at kfreeze 15 (1.05e28, gainq.py on the
final state) times |F| bounds Delta only to 3.6e-23. `reconv622.sh` re-converges that system from the h15 state
(I1098-mm5/ladder/D622/tail/release_ls_h15_D622.0000.npz, blob 7209f398, copied here as h15_D622.npz) to tol 1e-62
by release_ls --harm 15 --kmax 15 (qq Jacobian, octo-double residual, 4 threads, fastmul6 site_y). Its last target
|F| and its change of Delta from the h15 state give D 622's err_resid.
