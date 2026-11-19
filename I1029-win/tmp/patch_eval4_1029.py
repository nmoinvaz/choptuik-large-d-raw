p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\eval_1029.py"
s = open(p, encoding="utf-8").read()
old = "    return K, Jf, f, fixed\n"
assert old in s
s = s.replace(old, "    f = {k: (z if isinstance(z, mp.mpc) else mp.mpc(z.real, z.imag)) for k, z in f.items()}      # every sum in mpmath: a double product of f and A^k overflows past 1e308\n    return K, Jf, f, fixed\n", 1)
open(p, "w", encoding="utf-8").write(s)
