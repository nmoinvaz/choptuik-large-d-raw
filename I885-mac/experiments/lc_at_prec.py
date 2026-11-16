"""run b8m_lc.py with the B8 chain's working precision set to sys.argv[1] bits (b8m_atoms.atoms' default)"""
import runpy
import sys
prec = int(sys.argv[1])
sys.argv = ["b8m_lc.py"] + sys.argv[2:]
sys.path.insert(0, ".")
import b8m_atoms
d = list(b8m_atoms.atoms.__defaults__)
assert d[2] == 256, d
d[2] = prec
b8m_atoms.atoms.__defaults__ = tuple(d)
runpy.run_path("b8m_lc.py", run_name="__main__")
