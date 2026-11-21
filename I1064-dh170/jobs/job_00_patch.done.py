import glob
_orig = getattr(glob, "_orig_glob", glob.glob)
glob._orig_glob = _orig
glob.glob = lambda p, *a, **k: [f for f in _orig(p, *a, **k) if ".done" not in f]
print("patched glob in the worker: files with .done are skipped")
